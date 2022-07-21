from edc_screening.screening_eligibility import FC, ScreeningEligibility


class EligibilityPartTwo(ScreeningEligibility):

    eligible_fld_name = "eligible_part_two"
    reasons_ineligible_fld_name = "reasons_ineligible_part_two"

    def __init__(self, **kwargs):
        self.acute_condition = None
        self.acute_metabolic_acidosis = None
        self.advised_to_fast = None
        self.alcoholism = None
        self.appt_datetime = None
        self.congestive_heart_failure = None
        self.has_dm = None
        self.on_dm_medication = None
        self.liver_disease = None
        self.metformin_sensitivity = None
        self.renal_function_condition = None
        self.tissue_hypoxia_condition = None
        super().__init__(**kwargs)

    def get_required_fields(self) -> dict[str, FC]:
        return {}

    def set_eligible_model_field(self):
        setattr(self.model_obj, self.eligible_fld_name, self.eligible)
