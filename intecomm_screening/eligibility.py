from edc_constants.constants import FEMALE, MALE, NO, YES
from edc_screening.fc import FC
from edc_screening.screening_eligibility import ScreeningEligibility as Base


class ScreeningEligibility(Base):

    eligible_fld_name = "eligiblee"
    reasons_ineligible_fld_name = "reasons_ineligible"

    def __init__(self, **kwargs):
        self.age_in_years = None
        self.patient_conditions = None
        self.gender = None
        self.fasted = None
        self.staying_nearby_6 = None
        super().__init__(**kwargs)

    def get_required_fields(self) -> dict[str, FC]:
        return {
            "age_in_years": FC(range(18, 120), "age<18"),
            "gender": FC([MALE, FEMALE], "gender invalid"),
            "patient_conditions": FC([YES], "Must have at-least on condition"),
            "staying_nearby_6": FC(YES, "Unable/Unwilling to stay nearby for 6m"),
        }

    def set_fld_attrs_on_model(self) -> None:
        if self.eligible == YES:
            self.model_obj.continue_part_two = YES
        else:
            self.model_obj.continue_part_two = NO

    def set_eligible_model_field(self):
        setattr(self.model_obj, self.eligible_fld_name, self.eligible)
