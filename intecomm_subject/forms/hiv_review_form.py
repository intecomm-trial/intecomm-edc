from django import forms
from edc_constants.constants import NO, NOT_APPLICABLE, PENDING, YES
from edc_dx_review.utils import is_rx_initiated, raise_if_clinical_review_does_not_exist
from intecomm_form_validators.subject import HivReviewFormValidator

from ..models import HivReview
from .mixins import CrfModelFormMixin


class HivReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HivReviewFormValidator

    def clean(self):
        cleaned_data = super().clean()
        raise_if_clinical_review_does_not_exist(cleaned_data.get("subject_visit"))
        if is_rx_initiated(
            subject_identifier=self.get_subject_identifier(),
            report_datetime=self.report_datetime,
            instance_id=self.instance.id,
        ):
            if cleaned_data.get("rx_init") in [YES, NO]:
                raise forms.ValidationError(
                    {
                        "rx_init": (
                            "This field is applicable. Subject was NOT previously "
                            "reported as on ART."
                        )
                    }
                )

        elif cleaned_data.get("rx_init") == NOT_APPLICABLE:
            raise forms.ValidationError(
                {
                    "rx_init": (
                        "This field is applicable. Subject was NOT previously "
                        "reported as on ART."
                    )
                }
            )
        return cleaned_data

    def validate_viral_load(self):
        self.required_if(YES, PENDING, field="has_vl", field_required="drawn_date")
        if self.cleaned_data.get("drawn_date") and self.dx_date:
            if self.cleaned_data.get("drawn_date") < self.dx_date:
                raise forms.ValidationError(
                    {"drawn_date": "Invalid. Cannot be before HIV diagnosis."}
                )
        self.required_if(YES, field="has_vl", field_required="vl")
        self.required_if(YES, field="has_vl", field_required="vl_quantifier")

    class Meta:
        model = HivReview
        fields = "__all__"
        labels = {
            "has_vl": "Does the patient have a new or pending viral load result?",
            "vl": "Viral load result",
        }
        help_text = {"has_vl": "Do not report baseline results on this form."}
