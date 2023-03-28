from django import forms
from edc_constants.constants import YES
from edc_form_validators.form_validator import FormValidator
from inte_subject.forms.mixins import InitialReviewFormValidatorMixin
from respond_forms.utils import raise_if_clinical_review_does_not_exist

from ..constants import DRUGS, INSULIN
from ..models import DmInitialReview
from .mixins import (
    CrfFormValidatorMixin,
    CrfModelFormMixin,
    EstimatedDateFromAgoFormMixin,
    GlucoseFormValidatorMixin,
)


class DmInitialReviewFormValidator(
    InitialReviewFormValidatorMixin,
    GlucoseFormValidatorMixin,
    EstimatedDateFromAgoFormMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        self.raise_if_both_ago_and_actual_date()
        self.required_if(
            DRUGS,
            INSULIN,
            field="managed_by",
            field_required="med_start_ago",
        )

        if self.cleaned_data.get("dx_ago") and self.cleaned_data.get("med_start_ago"):
            if (
                self.estimated_date_from_ago("dx_ago")
                - self.estimated_date_from_ago("med_start_ago")
            ).days > 1:
                raise forms.ValidationError(
                    {"med_start_ago": "Invalid. Cannot be before diagnosis."}
                )
        self.required_if(YES, field="glucose_performed", field_required="glucose_date")
        self.validate_glucose_test()


class DmInitialReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmInitialReviewFormValidator

    class Meta:
        model = DmInitialReview
        fields = "__all__"
