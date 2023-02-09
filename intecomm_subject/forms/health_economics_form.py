from django import forms
from intecomm_form_validators.subject import HealthEconomicsFormValidator

from ..models import HealthEconomics
from .mixins import CrfModelFormMixin


class HealthEconomicsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsFormValidator

    class Meta:
        model = HealthEconomics
        fields = "__all__"
