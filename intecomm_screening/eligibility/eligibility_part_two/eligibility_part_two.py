from typing import Any

from edc_constants.constants import NO, TBD, YES

from ...constants import (
    FBG_INCOMPLETE,
    FBG_LT_13,
    NOT_STUDY_BP,
    NOT_STUDY_DM,
    STUDY_BP,
    STUDY_DM,
)
from .base_eligibility_part_two import BaseEligibilityPartTwo


class EligibilityPartTwo(BaseEligibilityPartTwo):
    def __init__(self, **kwargs):
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

    def set_fld_attrs_on_model(self: Any) -> None:
        """Set extra attr on the model"""
        super().set_fld_attrs_on_model()

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
