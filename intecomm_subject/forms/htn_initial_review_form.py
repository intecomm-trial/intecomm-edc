from django import forms
from intecomm_form_validators.subject import HtnInitialReviewFormValidator

from ..models import HtnInitialReview
from .mixins import CrfModelFormMixin


class HtnInitialReviewForm(
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HtnInitialReviewFormValidator

    class Meta:
        model = HtnInitialReview
        fields = "__all__"
