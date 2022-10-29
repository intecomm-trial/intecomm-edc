from edc_constants.constants import MALE, NO, YES
from edc_form_validators import INVALID_ERROR, FormValidator
from edc_screening.form_validator_mixins import SubjectScreeningFormValidatorMixin


class SubjectScreeningFormValidator(SubjectScreeningFormValidatorMixin, FormValidator):
    def clean(self):
        self.get_consent_for_period_or_raise()

        if (
            self.cleaned_data.get("consent_ability")
            and self.cleaned_data.get("consent_ability") == NO
        ):
            self.raise_validation_error(
                {
                    "consent_ability": (
                        "You may NOT screen this subject without their verbal consent."
                    )
                },
                INVALID_ERROR,
            )

        self.required_if(YES, field="in_care_6m", field_required="in_care_duration")
        self.applicable_if(YES, field="hiv_dx", field_applicable="hiv_dx_6m")
        self.required_if(YES, field="hiv_dx_6m", field_required="hiv_dx_ago")
        self.applicable_if(YES, field="hiv_dx", field_applicable="art_unchanged_3m")
        self.applicable_if(YES, field="hiv_dx", field_applicable="art_stable")
        self.applicable_if(YES, field="hiv_dx", field_applicable="art_adherent")

        self.applicable_if(YES, field="dm_dx", field_applicable="dm_dx_6m")
        self.required_if(YES, field="dm_dx_6m", field_required="dm_dx_ago")
        self.applicable_if(YES, field="dm_dx", field_applicable="dm_complications")

        self.applicable_if(YES, field="htn_dx", field_applicable="htn_dx_6m")
        self.required_if(YES, field="htn_dx_6m", field_required="htn_dx_ago")
        self.applicable_if(YES, field="htn_dx", field_applicable="htn_complications")

        self.not_applicable_if(
            MALE, field="gender", field_applicable="pregnant", inverse=False
        )

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )
