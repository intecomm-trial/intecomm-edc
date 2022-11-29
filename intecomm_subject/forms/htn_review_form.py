from django import forms
from intecomm_form_validators.subject import HtnReviewFormValidator

from ..models import HtnReview
from .mixins import CrfModelFormMixin


class HtnReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HtnReviewFormValidator

    class Meta:
        model = HtnReview
        fields = "__all__"
