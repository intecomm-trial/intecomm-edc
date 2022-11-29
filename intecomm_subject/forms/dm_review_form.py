from django import forms
from intecomm_form_validators.subject import DmReviewFormValidator

from ..models import DmReview
from .mixins import CrfModelFormMixin


class DmReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmReviewFormValidator

    class Meta:
        model = DmReview
        fields = "__all__"
