from __future__ import annotations

from typing import Dict

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import IntegrityError
from django.test import TestCase
from edc_constants.constants import FEMALE, MALE, NO, YES
from edc_utils import get_utcnow

from intecomm_consent.models import SubjectConsent
from intecomm_lists.models import ConsentRefusalReasons, ScreeningRefusalReasons
from intecomm_screening.exceptions import AlreadyConsentedError
from intecomm_screening.forms import (
    ConsentRefusalForm,
    PatientLogForm,
    SubjectScreeningForm,
)
from intecomm_screening.models import ConsentRefusal, SubjectScreening
from intecomm_screening.models.subject_screening import SubjectScreeningError
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin


class TestConsentRefusalModel(IntecommTestCaseMixin, TestCase):
    def test_consent_refusal_ok(self):
        subject_screening = self.get_subject_screening(
            patient_log_options=dict(willing_to_screen=YES)
        )
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)
        consent_refusal = self.get_consent_refusal(
            screening_identifier=subject_screening.screening_identifier
        )
        self.assertEqual(
            consent_refusal.screening_identifier,
            subject_screening.screening_identifier,
        )

    def test_consent_refusal_is_unique_by_screening_identifier(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(screening_identifier=subject_screening.screening_identifier)
        self.assertRaises(
            IntegrityError,
            self.get_consent_refusal,
            screening_identifier=subject_screening.screening_identifier,
        )

    def test_refusing_consent_after_consenting_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_subject_consent(subject_screening)
        self.assertRaises(
            AlreadyConsentedError,
            self.get_consent_refusal,
            screening_identifier=subject_screening.screening_identifier,
        )


class TestConsentRefusalForm(IntecommTestCaseMixin, TestCase):
    @staticmethod
    def get_refusal_data(screening_identifier: str | None = None) -> Dict:
        refusal_reason = ConsentRefusalReasons.objects.all()[0]
        return {
            "screening_identifier": screening_identifier,
            "report_datetime": get_utcnow(),
            "reason": refusal_reason,
            "other_reason": "",
            "site": Site.objects.get(id=settings.SITE_ID),
        }

    def test_consent_refusal_ok2(self):
        subject_screening = self.get_subject_screening(
            patient_log_options=dict(willing_to_screen=YES)
        )
        form = ConsentRefusalForm(
            data=self.get_refusal_data(
                screening_identifier=subject_screening.screening_identifier
            ),
            instance=ConsentRefusal(),
        )
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

    def test_screening_form_raises_if_patient_log_willing_to_screen_is_no(self):
        patient_log = self.get_patient_log(
            willing_to_screen=NO,
            screening_refusal_reason=ScreeningRefusalReasons.objects.get(
                name="dont_have_time"
            ),
        )
        form = SubjectScreeningForm(
            initial=dict(patient_log=patient_log), instance=SubjectScreening()
        )
        form.is_valid()
        self.assertIsNone(form._errors)
        self.assertRaises(
            SubjectScreeningError, self.get_subject_screening, patient_log=patient_log
        )

    def test_patient_log_cannot_be_changed_after_screen(self):
        patient_log = self.get_patient_log(willing_to_screen=YES, gender=FEMALE)
        self.get_subject_screening(patient_log=patient_log, gender=FEMALE)
        form = PatientLogForm(data=dict(gender=MALE), instance=patient_log)
        form.is_valid()
        self.assertIn("Patient has already screened", str(form._errors.get("__all__")))

    def test_refusal_after_already_refused_raises(self):
        subject_screening = self.get_subject_screening(
            patient_log_options=dict(willing_to_screen=YES)
        )
        refusal_form = ConsentRefusalForm(
            data=self.get_refusal_data(
                screening_identifier=subject_screening.screening_identifier
            ),
            instance=ConsentRefusal(),
        )
        refusal_form.is_valid()
        self.assertEqual(refusal_form._errors, {})
        refusal_form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

        refusal_form_two = ConsentRefusalForm(
            data=self.get_refusal_data(
                screening_identifier=subject_screening.screening_identifier
            ),
            instance=ConsentRefusal(),
        )
        refusal_form_two.is_valid()
        self.assertEqual(
            ["Consent Refusal with this Screening identifier already exists."],
            refusal_form_two._errors.get("screening_identifier"),
        )
        with self.assertRaises(ValueError):
            refusal_form_two.save()

        self.assertEqual(ConsentRefusal.objects.all().count(), 1)

    def test_raises_if_add_consent_refusal_after_already_consented(self):
        subject_screening = self.get_subject_screening(
            patient_log_options=dict(willing_to_screen=YES)
        )
        self.get_subject_consent(subject_screening=subject_screening)
        subject_screening.refresh_from_db()
        self.assertEqual(SubjectConsent.objects.all().count(), 1)

        refusal_form = ConsentRefusalForm(
            data=self.get_refusal_data(
                screening_identifier=subject_screening.screening_identifier
            ),
            instance=ConsentRefusal(),
        )
        refusal_form.is_valid()
        self.assertIn("__all__", refusal_form._errors)
        self.assertIn(
            "Not allowed. Subject has already consented. See subject ",
            refusal_form._errors.get("__all__")[0],
        )
        self.assertIn(
            subject_screening.subject_identifier,
            refusal_form._errors.get("__all__")[0],
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
            data=self.get_refusal_data(
                screening_identifier=subject_screening.screening_identifier
            ),
            instance=ConsentRefusal(),
        )
        refusal_form.is_valid()
        self.assertIn(
            "Not allowed. Subject is not eligible.",
            refusal_form._errors.get("__all__")[0],
        )
        self.assertIn(
            subject_screening.screening_identifier,
            refusal_form._errors.get("__all__")[0],
        )
        with self.assertRaises(ValueError):
            refusal_form.save()
        self.assertEqual(ConsentRefusal.objects.all().count(), 0)
