from django import forms
from intecomm_form_validators.subject import SocialHarmsFormValidator

from ..models import SocialHarms
from .mixins import CrfModelFormMixin


class SocialHarmsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = SocialHarmsFormValidator

    class Meta:
        model = SocialHarms
        fields = "__all__"
