from copy import deepcopy

from django.test import TestCase
from edc_constants.constants import NO, TBD, YES

from intecomm_screening.eligibility import EligibilityPartOne
from intecomm_screening.models import ScreeningPartOne

from ..options import get_part_one_eligible_options


class TestSubjectScreeningPartOneModel(TestCase):
    def test_eligibility_cls_eligible_yes(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        # cls attrs
        self.assertEqual(eligibility.eligible, YES)
        self.assertDictEqual(eligibility.reasons_ineligible, {})
        # model attrs
        self.assertIsNone(getattr(model_obj, EligibilityPartOne.reasons_ineligible_fld_name))
        self.assertEqual(
            getattr(model_obj, EligibilityPartOne.eligible_fld_name),
            EligibilityPartOne.is_eligible_value,
        )

    def test_eligibility_cls_missing_eligible_tbd(self):
        """Assert missing data does not assess, eligible==TBD"""

        # try as cleaned data
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(gender=None)
        eligibility = EligibilityPartOne(cleaned_data=part_one_eligible_options)
        self.assertEqual(eligibility.eligible, EligibilityPartOne.eligible_value_default)
        self.assertIn("gender", eligibility.reasons_ineligible)

        # try as model
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(gender=None)
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, TBD)
        self.assertIsNotNone(eligibility.reasons_ineligible)
        # model attrs
        self.assertIsNotNone(
            getattr(model_obj, EligibilityPartOne.reasons_ineligible_fld_name)
        )
        self.assertEqual(
            getattr(model_obj, EligibilityPartOne.eligible_fld_name),
            EligibilityPartOne.eligible_value_default,
        )

    def test_eligibility_cls_eligible_no(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        part_one_eligible_options.update(patient_conditions=NO)
        model_obj = ScreeningPartOne(**part_one_eligible_options)
        eligibility = EligibilityPartOne(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("patient_conditions", eligibility.reasons_ineligible)

    def test_defaults(self):
        opts = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**opts)
        obj.save()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)
        self.assertIsNotNone(obj.screening_identifier)

    def test_eligible(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        EligibilityPartOne(model_obj=obj)
        obj.save()
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_one, YES)

    def test_ineligible(self):
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        staying_nearby_6 = "staying_nearby_6"
        part_one_eligible_options.update({staying_nearby_6: NO})
        obj = ScreeningPartOne(**part_one_eligible_options)
        self.assertIsNone(obj.reasons_ineligible_part_one)
        obj.save()
        self.assertIn("Unable/Unwilling to stay nearby for", obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_one, NO)
        setattr(obj, staying_nearby_6, YES)
        obj.save()
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)
