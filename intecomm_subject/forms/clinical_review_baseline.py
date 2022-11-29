from django import forms
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_dx_review.form_validator_mixins import ClinicalReviewBaselineFormValidatorMixin
from edc_form_validators import FormValidator

from ..models import ClinicalReviewBaseline


class ClinicalReviewBaselineFormValidator(
    ClinicalReviewBaselineFormValidatorMixin, CrfFormValidatorMixin, FormValidator
):
    pass


class ClinicalReviewBaselineForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = ClinicalReviewBaselineFormValidator

    class Meta:
        model = ClinicalReviewBaseline
        fields = "__all__"
