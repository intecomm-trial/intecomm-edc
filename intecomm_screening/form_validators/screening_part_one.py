from django import forms
from edc_consent.form_validators import ConsentFormValidatorMixin
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator


class ScreeningPartOneFormValidator(ConsentFormValidatorMixin, FormValidator):
    def clean(self):

        self.get_consent_for_period_or_raise(self.cleaned_data.get("report_datetime"))

        self.required_if(NO, field="fasted", field_required="appt_datetime")

        if (
            not self.cleaned_data.get("screening_consent")
            or self.cleaned_data.get("screening_consent") != YES
        ):
            raise forms.ValidationError(
                {
                    "screening_consent": (
                        "You may NOT screen this subject without their verbal consent."
                    )
                }
            )
