from typing import Dict

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.test import TestCase, tag

from intecomm_consent.forms import SubjectConsentForm
from intecomm_consent.models import SubjectConsent
from intecomm_consent.utils import AlreadyConsentedError
from intecomm_lists.models import ConsentRefusalReasons
from intecomm_screening.forms import ConsentRefusalForm
from intecomm_screening.models import ConsentRefusal, Site, SubjectScreening
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin, now
from intecomm_screening.utils import AlreadyRefusedConsentError


@tag("sc")
class TestSubjectConsent(IntecommTestCaseMixin, TestCase):
    def test_consent_ok(self):
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)

    def test_consenting_more_than_once_raises(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)

        with self.assertRaises(AlreadyConsentedError) as cm:
            self.get_subject_consent(subject_screening)
        self.assertIn(
            f"Subject has already consented. See {subject_consent.subject_identifier}.",
            str(cm.exception),
        )

    def test_consenting_after_refusing_consent_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(subject_screening=subject_screening)

        with self.assertRaises(AlreadyRefusedConsentError) as cm:
            self.get_subject_consent(subject_screening)
        self.assertIn(
            "Patient has already refused consent. "
            f"See {subject_screening.screening_identifier}.",
            str(cm.exception),
        )


@tag("crf")
class TestSubjectConsentForm(IntecommTestCaseMixin, TestCase):
    def get_consent_data(self, subject_screening: SubjectScreening | None = None) -> Dict:
        subject_screening = subject_screening or self.get_subject_screening()
        return {
            "screening_identifier": subject_screening.screening_identifier,
            "subject_identifier": "not-sure-why-we-need-this",
            "report_datetime": now,
            "legal_name": subject_screening.legal_name,
            "familiar_name": subject_screening.familiar_name,
            "initials": subject_screening.initials,
            "gender": subject_screening.gender,
            "dob": (now.date() - relativedelta(years=subject_screening.age_in_years)),
            "site": Site.objects.get(id=settings.SITE_ID),
            "consent_datetime": subject_screening.report_datetime,
        }

    @tag("debug")
    def test_consent_ok(self):
        subject_screening = self.get_subject_screening()
        consent_form = SubjectConsentForm(
            data=self.get_consent_data(subject_screening=subject_screening),
            instance=None,
        )
        # TODO: fix
        consent_form.is_valid()
        self.assertEqual(consent_form.errors, {})
        consent_form.save()
        self.assertEqual(SubjectConsent.objects.all().count(), 1)

    def test_consent_after_already_consented_raises(self):
        # TODO:
        self.assertTrue(False, "TODO!")

    def test_consent_after_already_refused_raises(self):
        subject_screening = self.get_subject_screening()
        refusal_form = ConsentRefusalForm(
            data={
                "subject_screening": subject_screening,
                "report_datetime": now,
                "reason": ConsentRefusalReasons.objects.all()[0],
                "other_reason": "",
            },
            instance=None,
        )
        refusal_form.is_valid()
        self.assertEqual(refusal_form.errors, {})
        refusal_form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

        # TODO:
        self.assertTrue(False, "TODO!")

    def test_consent_if_not_eligible_raises(self):
        subject_screening = self.get_subject_screening()
        subject_screening.in_care_6m = False
        subject_screening.save()
        self.assertEqual(SubjectScreening.objects.all().count(), 1)

        # TODO:
        self.assertTrue(False, "TODO!")
