from decimal import Decimal
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
        self.assertEqual(obj.ratio, Decimal("0"))
        self.assertEqual(obj.randomize_now, NO)
        self.assertFalse(obj.randomized)
        self.assertEqual(obj.patients.all().count(), 0)

    @tag("grp1")
    def test_with_patients_ok(self):
        initials = "ABCDEFGHIJKLMNOP"
        for i in range(0, 4):
            make_recipe(
                "intecomm_screening.patientlog",
                name=f"NAME{i} AAA{i}",
                initials=f"N{initials[i]}A",
                hf_identifier=uuid4().hex,
                contact_number=f"123456789{i}",
                conditions=Conditions.objects.filter(name=HIV),
            )
        for i in range(0, 5):
            make_recipe(
                "intecomm_screening.patientlog",
                name=f"NAME{i} BBB{i}",
                initials=f"N{initials[i]}B",
                hf_identifier=uuid4().hex,
                contact_number=f"12345678{i}9",
                conditions=Conditions.objects.filter(name=DM),
            )
        for i in range(0, 5):
            make_recipe(
                "intecomm_screening.patientlog",
                name=f"NAME{i} CCC{i}",
                initials=f"N{initials[i]}C",
                hf_identifier=uuid4().hex,
                contact_number=f"1234567{i}89",
                conditions=Conditions.objects.filter(name=HTN),
            )

        obj = make_recipe("intecomm_screening.patientgroup")
        self.assertEqual(PatientLog.objects.all().count(), 14)
        for patient_log in PatientLog.objects.all():
            obj.patients.add(patient_log)

        for patient_log in PatientLog.objects.all():
            self.assertEqual(patient_log.patient_group.name, obj.name)

        obj.refresh_from_db()
        self.assertEqual(obj.patients.all().count(), 14)
