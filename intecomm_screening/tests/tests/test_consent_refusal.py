from typing import Dict

from django.test import TestCase, tag
from edc_utils import get_utcnow

from intecomm_consent.models import SubjectConsent
from intecomm_consent.utils import AlreadyConsentedError
from intecomm_lists.models import ConsentRefusalReasons
from intecomm_screening.forms import ConsentRefusalForm
from intecomm_screening.models import ConsentRefusal, SubjectScreening
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_screening.utils import AlreadyRefusedConsentError


@tag("cr")
class TestConsentRefusal(IntecommTestCaseMixin, TestCase):
    def test_consent_refusal_ok(self):
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        consent_refusal = self.get_consent_refusal(subject_screening=subject_screening)
        self.assertEqual(
            consent_refusal.screening_identifier,
            subject_screening.screening_identifier,
        )

    def test_refusing_consent_more_than_once_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(subject_screening=subject_screening)

        with self.assertRaises(AlreadyRefusedConsentError) as cm:
            self.get_consent_refusal(subject_screening=subject_screening)
        self.assertIn(
            "Patient has already refused consent. "
            f"See {subject_screening.screening_identifier}.",
            str(cm.exception),
        )

    def test_refusing_consent_after_consenting_raises(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)

        with self.assertRaises(AlreadyConsentedError) as cm:
            self.get_consent_refusal(subject_screening=subject_screening)
        self.assertIn(
            f"Subject has already consented. See {subject_consent.subject_identifier}.",
            str(cm.exception),
        )


@tag("crf")
class TestConsentRefusalForm(IntecommTestCaseMixin, TestCase):
    def get_refusal_data(self, subject_screening: SubjectScreening | None = None) -> Dict:
        refusal_reason = ConsentRefusalReasons.objects.all()[0]
        return {
            "subject_screening": subject_screening or self.get_subject_screening(),
            "report_datetime": get_utcnow(),
            "reason": refusal_reason,
            "other_reason": "",
        }

    def test_consent_refusal_ok(self):
        form = ConsentRefusalForm(data=self.get_refusal_data(), instance=None)
        form.is_valid()
        self.assertEqual(form.errors, {})
        form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

    def test_refusal_after_already_refused_raises(self):
        subject_screening = self.get_subject_screening()
        refusal_form = ConsentRefusalForm(
            data=self.get_refusal_data(subject_screening=subject_screening),
            instance=None,
        )
        refusal_form.is_valid()
        self.assertEqual(refusal_form.errors, {})
        refusal_form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

        refusal_form_two = ConsentRefusalForm(
            data=self.get_refusal_data(subject_screening=subject_screening),
            instance=None,
        )
        refusal_form_two.is_valid()
        self.assertIn("subject_screening", refusal_form_two.errors)
        self.assertEqual(
            ["Consent Refusal with this Subject screening already exists."],
            refusal_form_two.errors.get("subject_screening"),
        )
        with self.assertRaises(ValueError):
            refusal_form_two.save()

        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

    def test_refusal_after_already_consented_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_subject_consent(subject_screening=subject_screening)
        subject_screening.refresh_from_db()
        self.assertEqual(SubjectConsent.objects.all().count(), 1)

        refusal_form = ConsentRefusalForm(
            data=self.get_refusal_data(subject_screening=subject_screening),
            instance=ConsentRefusal(),
        )
        refusal_form.is_valid()
        self.assertIn("__all__", refusal_form.errors)
        self.assertIn(
            "Not allowed. Subject has already consented. See subject ",
            refusal_form.errors.get("__all__")[0],
        )
        self.assertIn(
            subject_screening.subject_identifier,
            refusal_form.errors.get("__all__")[0],
        )
        with self.assertRaises(ValueError):
            refusal_form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 0)

    def test_refusal_if_not_eligible_raises(self):
        subject_screening = self.get_subject_screening()
        subject_screening.in_care_6m = False
        subject_screening.save()
        self.assertEqual(SubjectScreening.objects.all().count(), 1)

        refusal_form = ConsentRefusalForm(
            data=self.get_refusal_data(subject_screening=subject_screening),
            instance=None,
        )
        refusal_form.is_valid()
        self.assertIn(
            "Not allowed. Subject is not eligible. See subject ",
            refusal_form.errors.get("__all__")[0],
        )
        self.assertIn(
            subject_screening.screening_identifier,
            refusal_form.errors.get("__all__")[0],
        )
        with self.assertRaises(ValueError):
            refusal_form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 0)
