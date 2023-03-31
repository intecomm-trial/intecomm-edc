from django import forms
from intecomm_form_validators.subject import DmInitialReviewFormValidator

from ..models import DmInitialReview
from .mixins import CrfModelFormMixin


class DmInitialReviewForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmInitialReviewFormValidator

    class Meta:
        model = DmInitialReview
        fields = "__all__"
