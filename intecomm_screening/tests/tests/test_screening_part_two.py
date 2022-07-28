from copy import deepcopy

from django.test import TestCase, tag
from edc_constants.constants import TBD, YES

from intecomm_screening.models import ScreeningPartOne, ScreeningPartTwo

from ..options import get_part_one_eligible_options, get_part_two_eligible_options


@tag("part2")
class TestScreeningPartTwo(TestCase):
    def setUp(self):
        """Complete parts one ..."""
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        obj.save()
        obj.refresh_from_db()
        self.screening_identifier = obj.screening_identifier

        # assert eligible for part one criteria
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)

        # assert eligible for part two criteria
        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertIsNotNone(obj.reasons_ineligible_part_two)
        self.assertIn(
            "FBG incomplete|sys_incomplete|diastolic_incomplete",
            obj.reasons_ineligible_part_two,
        )

        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def get_screening_part_two_obj(self):
        """Returns an SubjectScreening obj.

        Remember this is just a proxy model for SubjectScreening.
        """
        return ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier,
        )

    def test_eligible(self):
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        obj = self.get_screening_part_two_obj()
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertIsNone(obj.reasons_ineligible_part_two)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)

    def test_ineligible_fbg(self):
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        part_two_eligible_options["fbg_value"] = 14.0
        obj = self.get_screening_part_two_obj()
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertIn("high_fbg", obj.reasons_ineligible_part_two)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def test_ineligible_sys(self):
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        part_two_eligible_options["sys_blood_pressure"] = 165
        obj = self.get_screening_part_two_obj()
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertIn("high_systolic", obj.reasons_ineligible_part_two)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

    def test_ineligible_dia(self):
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        part_two_eligible_options["dia_blood_pressure"] = 110
        obj = self.get_screening_part_two_obj()
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertIn("high_diastolic", obj.reasons_ineligible_part_two)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
