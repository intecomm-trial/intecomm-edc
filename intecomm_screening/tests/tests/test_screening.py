from decimal import Decimal
from uuid import uuid4

from django.db import IntegrityError
from django.test import TestCase
from edc_constants.constants import DM, FEMALE, HIV, HTN, MALE, NO, UUID_PATTERN, YES
from intecomm_form_validators import RECRUITING
from model_bakery.baker import make_recipe

from intecomm_lists.models import Conditions, ScreeningRefusalReasons
from intecomm_screening.forms import PatientLogForm
from intecomm_screening.models import PatientLog, SubjectScreening
from intecomm_screening.models.subject_screening import SubjectScreeningError
from intecomm_screening.utils import InvalidScreeningIdentifier

from ..intecomm_test_case_mixin import IntecommTestCaseMixin


class TestScreening(IntecommTestCaseMixin, TestCase):
    def test_no_patients_ok(self):
        obj = make_recipe("intecomm_screening.patientgroup")
        self.assertEqual(obj.status, RECRUITING)
        self.assertIsNotNone(obj.name)
        self.assertIsNotNone(obj.group_identifier)
        self.assertRegexpMatches(str(obj.group_identifier), UUID_PATTERN)
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
            )
            obj.conditions.add(Conditions.objects.get(name=HIV))
        for i in range(0, 5):
            make_recipe(
                "intecomm_screening.patientlog",
                legal_name=f"NAMEB{i} BBB{i}",
                familiar_name=f"NAMEB{i}",
                hospital_identifier=uuid4().hex,
                contact_number=f"12345678{i}9",
            )
            obj.conditions.add(Conditions.objects.get(name=DM))
        for i in range(0, 5):
            make_recipe(
                "intecomm_screening.patientlog",
                legal_name=f"NAMEC{i} CCC{i}",
                familiar_name=f"NAMEC{i}",
                hospital_identifier=uuid4().hex,
                contact_number=f"1234567{i}89",
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
            screening_refusal_reason=ScreeningRefusalReasons.objects.get(
                name="dont_have_time"
            ),
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log=patient_log,
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
            screening_refusal_reason=None,
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log=patient_log,
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
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log=patient_log,
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
        )
        patient_log.conditions.add(Conditions.objects.get(name=HIV))
        subject_screening = SubjectScreening(
            patient_log=patient_log,
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
