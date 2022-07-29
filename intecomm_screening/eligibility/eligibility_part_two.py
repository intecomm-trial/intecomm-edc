from typing import Any

from edc_constants.constants import NO, TBD, YES
from edc_reportable import MILLIMOLES_PER_LITER, ConversionNotHandled, convert_units
from edc_screening.screening_eligibility import FC, ScreeningEligibility

from ..constants import FBG_INCOMPLETE


class EligibilityPartTwo(ScreeningEligibility):

    eligible_fld_name = "eligible_part_two"
    reasons_ineligible_fld_name = "reasons_ineligible_part_two"

    def __init__(self, **kwargs):
        self.fbg_units = None
        self.fbg_value = None
        self.sys_blood_pressure = None
        self.dia_blood_pressure = None
        self.unsuitable_agreed = None
        super().__init__(**kwargs)

    def assess_eligibility(self: Any) -> None:
        super().assess_eligibility()
        self.eligible = YES
        if not self.fbg_value:
            self.eligible = TBD
            self.reasons_ineligible.update(fbg_incomplete=FBG_INCOMPLETE)
        elif self.converted_fbg_value > 13:
            self.eligible = NO
            self.reasons_ineligible.update(high_fbg="high_fbg")
        if not self.sys_blood_pressure:
            self.eligible = TBD
            self.reasons_ineligible.update(sys_incomplete="sys_incomplete")
        elif self.sys_blood_pressure > 160:
            self.eligible = NO
            self.reasons_ineligible.update(high_systolic="high_systolic")
        if not self.dia_blood_pressure:
            self.eligible = TBD
            self.reasons_ineligible.update(diastolic_incomplete="diastolic_incomplete")
        elif self.dia_blood_pressure > 100:
            self.eligible = NO
            self.reasons_ineligible.update(high_diastolic="high_diastolic")

    def set_fld_attrs_on_model(self) -> None:
        self.model_obj.converted_fbg_value = self.converted_fbg_value

    def set_eligible_model_field(self):
        setattr(self.model_obj, self.eligible_fld_name, self.eligible)

    def get_required_fields(self) -> dict[str, FC]:
        return {
            "fbg_units": FC(ignore_if_missing=True),
            "fbg_value": FC(ignore_if_missing=True),
            "sys_blood_pressure": FC(ignore_if_missing=True),
            "dia_blood_pressure": FC(ignore_if_missing=True),
        }

    @property
    def converted_fbg_value(self) -> float:
        try:
            value = convert_units(
                self.fbg_value,
                units_from=self.fbg_units,
                units_to=MILLIMOLES_PER_LITER,
            )
        except ConversionNotHandled as e:
            raise ConversionNotHandled(f"FBG. {e}")
        return value
