from django import forms
from intecomm_form_validators.subject import ComplicationsFollowupFormValidators

from ..models import ComplicationsFollowup
from .mixins import CrfModelFormMixin


class ComplicationsFollowupForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ComplicationsFollowupFormValidators

    class Meta:
        model = ComplicationsFollowup
        fields = "__all__"
