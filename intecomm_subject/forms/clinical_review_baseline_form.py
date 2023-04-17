from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from intecomm_form_validators.subject import ClinicalReviewBaselineFormValidator

from ..models import ClinicalReviewBaseline


class ClinicalReviewBaselineForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalReviewBaselineFormValidator

    class Meta:
        model = ClinicalReviewBaseline
        fields = "__all__"
