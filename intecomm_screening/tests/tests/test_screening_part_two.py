from copy import deepcopy

from django.test import TestCase, tag
from edc_constants.constants import NO, TBD, YES
from edc_reportable import MILLIMOLES_PER_LITER, ConversionNotHandled
from edc_utils.date import get_utcnow

from intecomm_screening.models import ScreeningPartOne, ScreeningPartTwo

from ..options import get_part_one_eligible_options, get_part_two_eligible_options


class TestScreeningParttwo(TestCase):
    def setUp(self):
        """Complete parts one and two first ..."""
        part_one_eligible_options = deepcopy(get_part_one_eligible_options())
        obj = ScreeningPartOne(**part_one_eligible_options)
        obj.save()
        obj.refresh_from_db()
        self.screening_identifier = obj.screening_identifier

        # assert eligible for part one criteria
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_one)

        # assert eligible for part two criteria
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertIsNone(obj.reasons_ineligible_part_two)

        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)

    @tag("3")
    def get_screening_part_two_obj(self):
        """Returns an SubjectScreening obj.

        Remember this is just a proxy model for SubjectScreening.
        """
        return ScreeningPartTwo.objects.get(
            screening_identifier=self.screening_identifier,
        )

    def test_eligible_part_two_defaults_phase_two(self):
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        part_two_eligible_options["fbg_value"] = 6.9
        self._test_eligible(part_two_eligible_options)

    def _test_eligible(self, part_two_eligible_options):
        obj = self.get_screening_part_two_obj()
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        self.assertIsNone(obj.reasons_ineligible_part_two)
        self.assertEqual(obj.eligible_part_two, YES)

    def test_eligible_datetime_does_not_change_on_resave(self):
        obj = self.get_screening_part_two_obj()
        part_two_eligible_options = deepcopy(get_part_two_eligible_options())
        for k, v in part_two_eligible_options.items():
            setattr(obj, k, v)
        obj.save()
        obj.refresh_from_db()
        eligibility_datetime = obj.eligibility_datetime
        obj.save()
        obj.refresh_from_db()
        self.assertEqual(eligibility_datetime, obj.eligibility_datetime)

    def _test_eligible2(self, obj, incomplete_reason: str):
        self.assertIsNone(obj.reasons_ineligible_part_one)
        self.assertEqual(obj.eligible_part_one, YES)
        self.assertIsNone(obj.reasons_ineligible_part_two)
        self.assertEqual(obj.eligible_part_two, YES)

        self.assertEqual(obj.reasons_ineligible_part_two, incomplete_reason)
        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasting = NO
        obj.save()

        self.assertEqual(obj.reasons_ineligible_part_two, incomplete_reason)
        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        obj.fasting = YES
        obj.fasting_duration_str = "8h"
        obj.fbg_value = 6.9
        obj.fbg_units = MILLIMOLES_PER_LITER
        obj.fbg_datetime = get_utcnow()
        obj.save()

        self.assertEqual(obj.reasons_ineligible_part_two, incomplete_reason)
        self.assertEqual(obj.eligible_part_two, TBD)
        self.assertFalse(obj.eligible)
        self.assertFalse(obj.consented)

        try:
            obj.save()
        except ConversionNotHandled:
            pass
        else:
            self.fail("ConversionNotHandled unexpectedly not raised.")

        obj.save()

        self.assertFalse(obj.reasons_ineligible_part_two)
        self.assertEqual(obj.eligible_part_two, YES)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.consented)
