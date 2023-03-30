from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from intecomm_form_validators.subject import HivInitialReviewFormValidator

from ..models import HivInitialReview


class HivInitialReviewForm(
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HivInitialReviewFormValidator

    class Meta:
        model = HivInitialReview
        fields = "__all__"
