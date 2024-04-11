import re
from decimal import Decimal
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import IntegrityError
from django.test import TestCase, override_settings, tag
from edc_constants.constants import (
    DM,
    FEMALE,
    HIV,
    HTN,
    MALE,
    NO,
    TBD,
    UUID_PATTERN,
    YES,
)
from intecomm_form_validators import RECRUITING
from model_bakery.baker import make_recipe

from intecomm_lists.models import Conditions, ScreeningRefusalReasons
from intecomm_screening.forms import PatientLogForm, SubjectScreeningForm
from intecomm_screening.models import PatientLog, SubjectScreening
from intecomm_screening.models.subject_screening import SubjectScreeningError
from intecomm_screening.utils import InvalidScreeningIdentifier

from ..intecomm_test_case_mixin import IntecommTestCaseMixin


class TestScreening(IntecommTestCaseMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.user.refresh_from_db()
        self.user.userprofile.sites.add(Site.objects.get(id=101))

    def test_no_patients_ok(self):
        obj = make_recipe("intecomm_screening.patientgroup")
        self.assertEqual(obj.status, RECRUITING)
        self.assertIsNotNone(obj.name)
        self.assertIsNotNone(obj.group_identifier)
        self.assertTrue(re.match(UUID_PATTERN, str(obj.group_identifier)))
        self.assertEqual(obj.ratio, Decimal("0"))
        self.assertEqual(obj.randomize_now, NO)
        self.assertFalse(obj.randomized)
        self.assertEqual(obj.patients.all().count(), 0)

    def test_with_patients_ok(self):
        obj = None
        initials = "ABCDEFGHIJKLMNOP"
        for i in range(0, 4):
            obj = make_recipe(
                "intecomm_screening.patientlog",
                legal_name=f"NAMEA{i} AAA{i}",
                familiar_name=f"NAMEA{i}",
                initials=f"N{initials[i]}A",
                hospital_identifier=uuid4().hex,
                contact_number=f"123456789{i}",
                site_id=settings.SITE_ID,
            )
            obj.conditions.add(Conditions.objects.get(name=HIV))
        for i in range(0, 5):
            make_recipe(
                "intecomm_screening.patientlog",
                legal_name=f"NAMEB{i} BBB{i}",
                familiar_name=f"NAMEB{i}",
                hospital_identifier=uuid4().hex,
                contact_number=f"12345678{i}9",
                site_id=settings.SITE_ID,
            )
            obj.conditions.add(Conditions.objects.get(name=DM))
        for i in range(0, 5):
            make_recipe(
                "intecomm_screening.patientlog",
                legal_name=f"NAMEC{i} CCC{i}",
                familiar_name=f"NAMEC{i}",
                hospital_identifier=uuid4().hex,
                contact_number=f"1234567{i}89",
                site_id=settings.SITE_ID,
            )
            obj.conditions.add(Conditions.objects.get(name=HTN))
        for patient_log in PatientLog.objects.all():
            self.assertEqual(patient_log.patientgroup_set.all().count(), 0)
        self.assertEqual(PatientLog.objects.all().count(), 14)

        # create patient_group
        patient_group = make_recipe("intecomm_screening.patientgroup")

        # add patient_logs to patient_group
        for index, patient_log in enumerate(PatientLog.objects.all()):
            patient_group.patients.add(patient_log)
        for patient_log in PatientLog.objects.all():
            self.assertEqual(patient_log.patientgroup_set.all().count(), 1)
            self.assertEqual(patient_log.patientgroup_set.all().first(), patient_group)

        patient_group.refresh_from_db()

        # TODO: why does this fail?
        # self.assertEqual(patient_group.patients.count(), 14)

    def test_screening_raises_if_unwilling_in_patient_log(self):
        patient_log = make_recipe(
            "intecomm_screening.patientlog",
            legal_name="NAMEA AAA",
            familiar_name="NAMEA",
            initials="NA",
            hospital_identifier=uuid4().hex,
            contact_number="1234567890",
            willing_to_screen=NO,
            screening_refusal_reason=ScreeningRefusalReasons.objects.get(
                name="dont_have_time"
            ),
            site_id=settings.SITE_ID,
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log_identifier=patient_log.patient_log_identifier,
            hospital_identifier=patient_log.hospital_identifier,
            gender=patient_log.gender,
            age_in_years=patient_log.age_in_years,
            legal_name=patient_log.legal_name,
            familiar_name=patient_log.familiar_name,
            initials=patient_log.initials,
        )

        with self.assertRaises(SubjectScreeningError) as cm:
            subject_screening.save()
        self.assertIn(
            f"Patient '{patient_log.patient_log_identifier}' is unwilling to screen.",
            str(cm.exception),
        )

    def test_screening_ok_if_not_unwilling_in_patient_log(self):
        patient_log = make_recipe(
            "intecomm_screening.patientlog",
            legal_name="NAMEA AAA",
            familiar_name="NAMEA",
            initials="NA",
            hospital_identifier=uuid4().hex,
            contact_number="1234567890",
            willing_to_screen=YES,
            screening_refusal_reason=None,
            site_id=settings.SITE_ID,
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log_identifier=patient_log.patient_log_identifier,
            hospital_identifier=patient_log.hospital_identifier,
            gender=patient_log.gender,
            age_in_years=patient_log.age_in_years,
            legal_name=patient_log.legal_name,
            familiar_name=patient_log.familiar_name,
            initials=patient_log.initials,
        )

        try:
            subject_screening.save()
        except SubjectScreeningError as e:
            self.fail(f"SubjectScreeningError unexpectedly raised. Got {e}")

    def test_screening_raises_if_hospital_identifier_mismatch(self):
        patient_log = make_recipe(
            "intecomm_screening.patientlog",
            legal_name="NAMEA AAA",
            familiar_name="NAMEA",
            initials="NA",
            hospital_identifier="56d2c5ebc7384309990ddc14ee2cf1b2",
            contact_number="1234567890",
            site_id=settings.SITE_ID,
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log_identifier=patient_log.patient_log_identifier,
            hospital_identifier="e8da3474883445cd906697d91e52a10a",
            gender=patient_log.gender,
            age_in_years=patient_log.age_in_years,
            legal_name=patient_log.legal_name,
            familiar_name=patient_log.familiar_name,
            initials=patient_log.initials,
        )

        with self.assertRaises(SubjectScreeningError) as cm:
            subject_screening.save()
        self.assertIn(
            "Health facility identifier does not match patient log. ",
            str(cm.exception),
        )

    def test_screening_raises_if_initials_mismatch(self):
        patient_log = make_recipe(
            "intecomm_screening.patientlog",
            legal_name="NAMEA AAA",
            familiar_name="NAMEA",
            initials="NA",
            hospital_identifier=uuid4().hex,
            contact_number="1234567890",
            site_id=settings.SITE_ID,
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log_identifier=patient_log.patient_log_identifier,
            hospital_identifier=patient_log.hospital_identifier,
            gender=patient_log.gender,
            age_in_years=patient_log.age_in_years,
            legal_name=patient_log.legal_name,
            familiar_name=patient_log.familiar_name,
            initials="XX",
        )

        with self.assertRaises(SubjectScreeningError) as cm:
            subject_screening.save()
        self.assertIn(
            "Initials do not match patient log. ",
            str(cm.exception),
        )

    def test_patient_log_gender_cannot_be_changed_after_screen(self):
        patient_log = self.get_patient_log(willing_to_screen=YES, gender=FEMALE)
        self.get_subject_screening(patient_log=patient_log, gender=FEMALE)
        form = PatientLogForm(data=dict(gender=MALE), instance=patient_log)
        form.is_valid()
        self.assertIn("Patient has already screened. Gender", str(form._errors.get("__all__")))

    def test_patient_log_initials_cannot_be_changed_after_screen(self):
        patient_log = self.get_patient_log(willing_to_screen=YES, gender=FEMALE, initials="YY")
        self.get_subject_screening(patient_log=patient_log, gender=FEMALE)
        form = PatientLogForm(data=dict(gender=FEMALE, initials="XX"), instance=patient_log)
        form.is_valid()
        self.assertIn(
            "Patient has already screened. Initials", str(form._errors.get("__all__"))
        )

    def test_screening_id_not_found_in_patient_log_raises(self):
        patient_log = self.get_patient_log()
        self.get_subject_screening(patient_log=patient_log)
        patient_log.screening_identifier = "some_other_identifier"
        self.assertRaises(InvalidScreeningIdentifier, patient_log.save)

    def test_patient_log_screening_identifier_unique_constraint(self):
        patient_log = self.get_patient_log()
        self.get_subject_screening(patient_log=patient_log)
        patient_log_two = self.get_patient_log(legal_name="NOTHER AME")
        patient_log_two.screening_identifier = patient_log.screening_identifier
        self.assertRaises(IntegrityError, patient_log_two.save)

    @override_settings(SITE_ID=101)
    def test_unwilling_to_screen_in_patient_log_raises(self):
        patient_log = self.get_patient_log(
            willing_to_screen=NO,
            screening_refusal_reason=ScreeningRefusalReasons.objects.get(
                name="dont_have_time"
            ),
            gender=FEMALE,
        )

        cleaned_data = dict(
            patient_log_identifier=patient_log.patient_log_identifier,
            gender=FEMALE,
        )
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertIn("Patient is unwilling to screen", str(form._errors.get("__all__", "")))

        patient_log.willing_to_screen = YES
        patient_log.screening_refusal_reason = None
        patient_log.save()
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertNotIn(
            "Patient is unwilling to screen", str(form._errors.get("__all__", ""))
        )

    @override_settings(SITE_ID=101)
    def test_gender(self):
        patient_log = self.get_patient_log(
            gender=FEMALE,
            willing_to_screen=YES,
            screening_refusal_reason=None,
        )
        cleaned_data = dict(
            gender=MALE, patient_log_identifier=patient_log.patient_log_identifier
        )
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertIn("Invalid. Expected Female", str(form._errors.get("gender", "")))

        cleaned_data = dict(
            gender=FEMALE, patient_log_identifier=patient_log.patient_log_identifier
        )
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertNotIn("gender", form._errors)

    @override_settings(SITE_ID=101)
    def test_initials(self):
        patient_log = self.get_patient_log(
            gender=FEMALE,
            initials="XX",
            willing_to_screen=YES,
            screening_refusal_reason=None,
        )
        cleaned_data = dict(
            patient_log_identifier=patient_log.patient_log_identifier,
            gender=FEMALE,
            initials="ZZ",
        )
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertIn("Invalid. Expected XX", str(form._errors.get("initials", "")))

        cleaned_data = dict(
            patient_log_identifier=patient_log.patient_log_identifier,
            gender=FEMALE,
            initials="XX",
        )
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertNotIn("initials", form._errors)

    @tag("1")
    @override_settings(SITE_ID=101)
    def test_conditions_matching_patient_log(self):
        patient_log = self.get_patient_log(
            gender=MALE,
            age_in_years=20,
            initials="XX",
            willing_to_screen=YES,
            screening_refusal_reason=None,
            hospital_identifier="123456789",
            conditions=[DM],
            site=Site.objects.get(id=settings.SITE_ID),
        )
        cleaned_data = dict(
            report_datetime=patient_log.report_datetime,
            patient_log_identifier=patient_log.patient_log_identifier,
            gender=MALE,
            age_in_years=20,
            initials="XX",
            hospital_identifier="123456789",
            consent_ability=YES,
            in_care_6m=YES,
            in_care_duration="5y",
            hiv_dx=NO,
            dm_dx=YES,
            htn_dx=YES,
            site=Site.objects.get(id=settings.SITE_ID),
        )
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertIn("Invalid. Condition not indicated", str(form._errors.get("htn_dx", "")))

        patient_log.conditions.add(Conditions.objects.get(name=HTN))
        patient_log.save()
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertNotIn(
            "Invalid. Condition not indicated", str(form._errors.get("hiv_dx", ""))
        )
        self.assertNotIn(
            "Invalid. Condition not indicated", str(form._errors.get("htn_dx", ""))
        )
        self.assertNotIn(
            "Invalid. Condition not indicated", str(form._errors.get("dm_dx", ""))
        )

        patient_log.conditions.remove(Conditions.objects.get(name=HIV))
        patient_log.conditions.remove(Conditions.objects.get(name=HTN))
        patient_log.conditions.remove(Conditions.objects.get(name=DM))
        patient_log.save()
        cleaned_data.update(hiv_dx=NO, dm_dx=NO, htn_dx=NO)
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertIn(
            "No conditions (HIV/DM/HTN) have been indicated for this patient",
            str(form._errors.get("__all__", "")),
        )

    @override_settings(SITE_ID=101)
    def test_health_talk_reponse_from_patientlog(self):
        patient_log = self.get_patient_log(
            gender=MALE,
            age_in_years=20,
            initials="XX",
            willing_to_screen=YES,
            screening_refusal_reason=None,
            conditions=[DM],
            first_health_talk=TBD,
            second_health_talk=TBD,
        )
        cleaned_data = dict(
            report_datetime=patient_log.report_datetime,
            patient_log_identifier=patient_log.patient_log_identifier,
            gender=MALE,
            age_in_years=20,
            initials="XX",
            consent_ability=YES,
            in_care_6m=YES,
            in_care_duration="5y",
            hiv_dx=NO,
            dm_dx=YES,
            htn_dx=NO,
        )
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertIn(
            "Has patient attended the first health talk", str(form._errors.get("__all__", ""))
        )

        patient_log.first_health_talk = YES
        patient_log.second_health_talk = TBD
        patient_log.save()
        patient_log.refresh_from_db()

        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()
        self.assertIn(
            "Has patient attended the second health talk", str(form._errors.get("__all__", ""))
        )

        patient_log.first_health_talk = NO
        patient_log.second_health_talk = NO
        patient_log.save()
        patient_log.refresh_from_db()
        form = SubjectScreeningForm(data=cleaned_data, instance=SubjectScreening())
        form.is_valid()

        self.assertNotIn(
            "Has patient attended the first health talk", str(form._errors.get("__all__", ""))
        )
        self.assertNotIn(
            "Has patient attended the second health talk", str(form._errors.get("__all__", ""))
        )
