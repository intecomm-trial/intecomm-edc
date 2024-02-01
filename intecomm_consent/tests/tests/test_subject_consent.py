from __future__ import annotations

from typing import Dict

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import IntegrityError
from django.test import TestCase, override_settings, tag
from edc_consent.constants import HOSPITAL_NUMBER
from edc_constants.constants import NO, NOT_APPLICABLE, YES

from intecomm_consent.forms import SubjectConsentTzForm, SubjectConsentUgForm
from intecomm_consent.models import SubjectConsentTz, SubjectConsentUg
from intecomm_lists.models import ScreeningRefusalReasons
from intecomm_screening.models import ConsentRefusal, Site, SubjectScreening
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin, now
from intecomm_screening.utils import AlreadyRefusedConsentError


class TestSubjectConsent(IntecommTestCaseMixin, TestCase):
    def test_consent_ok(self):
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)

    def test_consenting_when_screened_despite_unwilling_to_screen_raises(self):
        patient_log = self.get_patient_log(willing_to_screen=YES)
        subject_screening = self.get_subject_screening(patient_log=patient_log)
        patient_log.willing_to_screen = NO
        patient_log.screening_refusal_reason = ScreeningRefusalReasons.objects.get(
            name="dont_have_time"
        )
        patient_log.save()
        self.get_subject_consent(subject_screening=subject_screening)
        self.assertRaises(
            IntegrityError, self.get_subject_consent, subject_screening=subject_screening
        )

    def test_consenting_more_than_once_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_subject_consent(subject_screening)
        self.assertRaises(IntegrityError, self.get_subject_consent, subject_screening)

    def test_consenting_after_refusing_consent_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(screening_identifier=subject_screening.screening_identifier)

        with self.assertRaises(AlreadyRefusedConsentError) as cm:
            self.get_subject_consent(subject_screening)
        self.assertIn(
            "Patient has already refused to consent. "
            f"See {subject_screening.screening_identifier}.",
            str(cm.exception),
        )


class TestSubjectConsentForm(IntecommTestCaseMixin, TestCase):
    def get_consent_data(self, subject_screening: SubjectScreening | None = None) -> Dict:
        subject_screening = subject_screening or self.get_subject_screening()
        return {
            "screening_identifier": subject_screening.screening_identifier,
            "subject_identifier": "123-456-789",
            "report_datetime": now,
            "legal_name": subject_screening.legal_name,
            "familiar_name": subject_screening.familiar_name,
            "initials": subject_screening.initials,
            "gender": subject_screening.gender,
            "language": "en",
            "is_literate": YES,
            "consent_datetime": subject_screening.report_datetime,
            "dob": (now.date() - relativedelta(years=subject_screening.age_in_years)),
            "is_dob_estimated": "-",
            "identity": "123/456/789",
            "identity_type": HOSPITAL_NUMBER,
            "confirm_identity": "123/456/789",
            "is_incarcerated": NO,
            # Review questions
            "consent_reviewed": YES,
            "study_questions": YES,
            "assessment_score": YES,
            "consent_signature": YES,
            "consent_copy": YES,
            # Group
            "group_identifier": "G123-456",
            # Other stuff not included in admin class
            "site": Site.objects.get(id=settings.SITE_ID),
            "citizen": NO,
            "legal_marriage": NOT_APPLICABLE,
            "marriage_certificate": NOT_APPLICABLE,
            "subject_type": "subject",
            "may_store_genetic_samples": NO,
            "may_store_samples": NO,
        }

    @override_settings(SITE_ID=201)
    def test_consent_ok(self):
        subject_screening = self.get_subject_screening()
        consent_form = SubjectConsentTzForm(
            data=self.get_consent_data(subject_screening=subject_screening),
            initial={"screening_identifier": subject_screening.screening_identifier},
            instance=SubjectConsentTz(),
        )
        consent_form.is_valid()
        self.assertEqual(consent_form._errors, {})
        consent_form.save()
        self.assertEqual(SubjectConsentTz.objects.all().count(), 1)

    @override_settings(SITE_ID=101)
    def test_consent_ug_ok(self):
        subject_screening = self.get_subject_screening()
        consent_form = SubjectConsentUgForm(
            data=self.get_consent_data(subject_screening=subject_screening),
            initial={"screening_identifier": subject_screening.screening_identifier},
            instance=SubjectConsentUg(),
        )
        consent_form.is_valid()
        self.assertEqual(consent_form._errors, {})
        consent_form.save()
        self.assertEqual(SubjectConsentUg.objects.all().count(), 1)

    @tag("1")
    @override_settings(SITE_ID=201)
    def test_consent_after_already_consented_raises(self):
        subject_screening = self.get_subject_screening()
        consent_form = SubjectConsentTzForm(
            data=self.get_consent_data(subject_screening=subject_screening),
            initial={"screening_identifier": subject_screening.screening_identifier},
            instance=SubjectConsentTz(),
        )
        consent_form.is_valid()
        self.assertEqual(consent_form._errors, {})
        consent_form.save()
        self.assertEqual(SubjectConsentTz.objects.all().count(), 1)

        consent_form_two = SubjectConsentTzForm(
            data=self.get_consent_data(subject_screening=subject_screening),
            initial={"screening_identifier": subject_screening.screening_identifier},
            instance=SubjectConsentTz(),
        )
        consent_form_two.is_valid()
        self.assertNotEqual(consent_form_two._errors, {})
        self.assertIn("screening_identifier", consent_form_two._errors)
        self.assertEqual(
            ["Subject Consent with this Screening identifier already exists."],
            consent_form_two._errors.get("screening_identifier"),
        )
        with self.assertRaises(ValueError):
            consent_form_two.save()
        self.assertEqual(SubjectConsentTz.objects.all().count(), 1)

    @override_settings(SITE_ID=201)
    def test_consent_after_already_refused_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(screening_identifier=subject_screening.screening_identifier)
        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

        consent_form = SubjectConsentTzForm(
            data=self.get_consent_data(subject_screening=subject_screening),
            initial={"screening_identifier": subject_screening.screening_identifier},
            instance=SubjectConsentTz(),
        )
        consent_form.is_valid()
        self.assertNotEqual(consent_form._errors, {})
        self.assertIn("__all__", consent_form._errors)
        self.assertIn(
            "Not allowed. Patient has already refused consent. See subject ",
            consent_form._errors.get("__all__")[0],
        )
        self.assertIn(
            str(ConsentRefusal.objects.get(subject_screening_id=subject_screening.id).id),
            consent_form._errors.get("__all__")[0],
        )
        self.assertIn(
            subject_screening.screening_identifier,
            consent_form._errors.get("__all__")[0],
        )
        with self.assertRaises(ValueError):
            consent_form.save()
        self.assertEqual(SubjectConsentTz.objects.all().count(), 0)

    @override_settings(SITE_ID=201)
    def test_consent_if_not_eligible_raises(self):
        subject_screening = self.get_subject_screening()
        subject_screening.in_care_6m = False
        subject_screening.save()
        self.assertFalse(subject_screening.eligible)
        consent_form = SubjectConsentTzForm(
            data=self.get_consent_data(subject_screening=subject_screening),
            initial={"screening_identifier": subject_screening.screening_identifier},
            instance=SubjectConsentTz(),
        )
        consent_form.is_valid()
        self.assertNotEqual(consent_form._errors, {})
        self.assertIn("__all__", consent_form._errors)
        self.assertIn("Subject is not eligible", consent_form._errors.get("__all__")[0])
