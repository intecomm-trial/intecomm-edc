from copy import deepcopy

from django.test import TestCase, tag
from edc_constants.constants import NO, YES

from intecomm_screening.eligibility import ScreeningEligibility
from intecomm_screening.models import SubjectScreening

from ..options import get_eligible_options


class TestSubjectScreening(TestCase):
    @tag("1")
    def test_defaults(self):
        opts = deepcopy(get_eligible_options())
        obj = SubjectScreening(**opts)
        obj.save()
        self.assertEqual(obj.eligible, YES)
        self.assertIsNone(obj.reasons_ineligible)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)
        self.assertIsNotNone(obj.screening_identifier)

    def test_eligibility_part_one(self):
        eligible_options = deepcopy(get_eligible_options())
        model_obj = SubjectScreening(**eligible_options)
        eligibility = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, YES)
        self.assertDictEqual(eligibility.reasons_ineligible, {})
        self.assertIsNone(getattr(model_obj, ScreeningEligibility.reasons_ineligible_fld_name))
        self.assertEqual(
            getattr(model_obj, ScreeningEligibility.eligible_fld_name),
            ScreeningEligibility.is_eligible_value,
        )

    def test_ineligibility_patient_conditions(self):
        eligible_options = deepcopy(get_eligible_options())
        eligible_options.update(patient_conditions=NO)
        model_obj = SubjectScreening(**eligible_options)
        eligibility = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("patient_conditions", eligibility.reasons_ineligible)

    def test_ineligibility_staying_nearby_6(self):
        eligible_options = deepcopy(get_eligible_options())
        eligible_options.update(staying_nearby_6=NO)
        model_obj = SubjectScreening(**eligible_options)
        eligibility = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("staying_nearby_6", eligibility.reasons_ineligible)

    def test_ineligibility_age(self):
        eligible_options = deepcopy(get_eligible_options())
        eligible_options.update(age_in_years=17)
        model_obj = SubjectScreening(**eligible_options)
        eligibility = ScreeningEligibility(model_obj=model_obj)
        self.assertEqual(eligibility.eligible, NO)
        self.assertIn("age_in_years", eligibility.reasons_ineligible)

    def test_eligible(self):
        eligible_options = deepcopy(get_eligible_options())
        obj = SubjectScreening(**eligible_options)
        ScreeningEligibility(model_obj=obj)
        obj.save()
        self.assertIsNone(obj.reasons_ineligible)
        self.assertEqual(obj.eligible, YES)
