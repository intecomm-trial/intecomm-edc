from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from intecomm_form_validators.subject.clinical_review_form_validator import (
    ClinicalReviewFormValidator,
)

from ..models import ClinicalReview


class ClinicalReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalReviewFormValidator

    class Meta:
        model = ClinicalReview
        fields = "__all__"
