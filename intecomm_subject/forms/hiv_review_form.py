from django import forms
from intecomm_form_validators.subject import HivReviewFormValidator

from ..models import HivReview
from .mixins import CrfModelFormMixin


class HivReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HivReviewFormValidator

    class Meta:
        model = HivReview
        fields = "__all__"
