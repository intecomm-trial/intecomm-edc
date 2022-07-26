from edc_reportable import MILLIMOLES_PER_LITER, ConversionNotHandled, convert_units
from edc_screening.screening_eligibility import FC, ScreeningEligibility


class BaseEligibilityPartTwo(ScreeningEligibility):
    eligible_fld_name = "eligible_part_two"
    reasons_ineligible_fld_name = "reasons_ineligible_part_two"

    def __init__(self, **kwargs):
        self.fbg_units = None
        self.fbg_value = None
        self.sys_blood_pressure_one = None
        self.unsuitable_agreed = None
        super().__init__(**kwargs)

    def assess_eligibility(self) -> None:
        pass
        # if self.weight and self.height:
        #     self.bmi = calculate_bmi(weight_kg=self.weight, height_cm=self.height)
        # self.calculated_egfr_value = EgfrCkdEpi(**self.model_obj.__dict__).value

    def set_fld_attrs_on_model(self) -> None:
        self.model_obj.converted_fbg_value = self.converted_fbg_value

    def get_required_fields(self) -> dict[str, FC]:
        return {
            "fbg_units": FC(ignore_if_missing=True),
            "fbg_value": FC(ignore_if_missing=True),
        }

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

    def set_eligible_model_field(self):
        setattr(self.model_obj, self.eligible_fld_name, self.eligible)
