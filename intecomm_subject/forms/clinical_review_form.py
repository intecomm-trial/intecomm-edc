from django import forms
from edc_constants.constants import YES
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_dx_review.form_validator_mixins import ClinicalReviewFollowupFormValidatorMixin
from edc_form_validators import FormValidator
from edc_visit_schedule.utils import raise_if_baseline

from ..models import ClinicalReview


class ClinicalReviewFormValidator(
    ClinicalReviewFollowupFormValidatorMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        raise_if_baseline(self.cleaned_data.get("subject_visit"))
        self.required_if(
            YES,
            field="health_insurance",
            field_required="health_insurance_monthly_pay",
        )
        self.required_if(
            YES,
            field="patient_club",
            field_required="patient_club_monthly_pay",
        )


class ClinicalReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalReviewFormValidator

    class Meta:
        model = ClinicalReview
        fields = "__all__"
