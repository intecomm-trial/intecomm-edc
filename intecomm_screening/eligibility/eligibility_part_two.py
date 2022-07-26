from typing import Any

from edc_constants.constants import NO, TBD, YES
from edc_reportable import MILLIMOLES_PER_LITER, ConversionNotHandled, convert_units
from edc_screening.screening_eligibility import FC, ScreeningEligibility

from ..constants import FBG_INCOMPLETE, FBG_LT_13, NOT_STUDY_DM, STUDY_DM


class EligibilityPartTwo(ScreeningEligibility):

    eligible_fld_name = "eligible_part_two"
    reasons_ineligible_fld_name = "reasons_ineligible_part_two"

    def __init__(self, **kwargs):
        self.fbg_units = None
        self.fbg_value = None
        self.sys_blood_pressure_one = None
        self.unsuitable_agreed = None
        super().__init__(**kwargs)

    def assess_eligibility(self: Any) -> None:
        super().assess_eligibility()
        if not self.fbg_category:
            self.eligible = TBD
            self.reasons_ineligible.update(fbg_incomplete=FBG_INCOMPLETE)
        else:
            if self.fbg_category == STUDY_DM:
                self.eligible = YES
            else:
                self.eligible = NO
                self.reasons_ineligible.update(fbg_low=FBG_LT_13)

    def set_fld_attrs_on_model(self) -> None:
        self.model_obj.converted_fbg_value = self.converted_fbg_value

    def get_required_fields(self) -> dict[str, FC]:
        return {
            "fbg_units": FC(ignore_if_missing=True),
            "fbg_value": FC(ignore_if_missing=True),
        }

    @property
    def fbg_category(self):
        # FBG>13 mmol/L
        value = self.converted_fbg_value
        if not value:
            fbg_category = None
        elif value <= 13:
            fbg_category = NOT_STUDY_DM
        elif value > 13:
            fbg_category = STUDY_DM
        else:
            raise ValueError("Invalid FBG value")
        return fbg_category

    @property
    def converted_fbg_value(self):
        try:
            value = convert_units(
                self.fbg_value,
                units_from=self.fbg_units,
                units_to=MILLIMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"FBG. {e}")
        return value
