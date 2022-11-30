from uuid import uuid4

from django.test import TestCase, tag
from edc_constants.constants import DM, HIV, HTN, NO, UUID_PATTERN
from intecomm_form_validators import RECRUITING
from model_bakery.baker import make_recipe

from intecomm_lists.models import Conditions
from intecomm_screening.models import PatientLog


class TestScreening(TestCase):
    def test_no_patients_ok(self):
        obj = make_recipe("intecomm_screening.patientgroup")
        self.assertEqual(obj.status, RECRUITING)
        self.assertIsNotNone(obj.name)
        self.assertIsNotNone(obj.group_identifier)
        self.assertRegexpMatches(str(obj.group_identifier), UUID_PATTERN)
        self.assertEqual(obj.ratio, None)
        self.assertEqual(obj.randomize_now, NO)
        self.assertFalse(obj.randomized)
        self.assertEqual(obj.patients.all().count(), 0)

    @tag("grp1")
    def test_with_patients_ok(self):
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
