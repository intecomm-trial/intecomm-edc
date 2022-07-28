from copy import deepcopy

from django.test import TestCase, tag
from edc_constants.constants import NO, YES

from intecomm_screening.eligibility import EligibilityPartOne
from intecomm_screening.models import ScreeningPartOne

from ..options import get_part_one_eligible_options


@tag("part1")
class TestSubjectScreeningPartOneModel(TestCase):
    def test_defaults(self):
        opts = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**opts)
        obj.save()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
        self.assertIsNotNone(obj.screening_identifier)

    def test_eligibility_part_one(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, YES)
        self.assertDictEqual(eligibility.reasons_ineligible, {})
        self.assertIsNone(getattr(model_obj, EligibilityPartOne.reasons_ineligible_fld_name))
        self.assertEqual(
            getattr(model_obj, EligibilityPartOne.eligible_fld_name),
            EligibilityPartOne.is_eligible_value,
        )

    def test_ineligibility_patient_conditions(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(patient_conditions=NO)
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("patient_conditions", eligibility.reasons_ineligible)

    def test_ineligibility_staying_nearby_6(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(staying_nearby_6=NO)
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("staying_nearby_6", eligibility.reasons_ineligible)

    def test_ineligibility_age(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(age_in_years=17)
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("age_in_years", eligibility.reasons_ineligible)

    def test_eligible(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        EligibilityPartOne(model_obj=obj)
        obj.save()
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_one, YES)
