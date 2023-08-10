from django import forms
from edc_constants.constants import NO, NOT_APPLICABLE, YES
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
            subject_identifier=self.subject_identifier,
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

    class Meta:
        model = HivReview
        fields = "__all__"
