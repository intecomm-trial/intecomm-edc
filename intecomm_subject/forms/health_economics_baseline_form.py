from django import forms
from intecomm_form_validators.subject import HealthEconomicsBaselineFormValidator

from ..models import HealthEconomicsBaseline
from .mixins import CrfModelFormMixin


class HealthEconomicsBaselineForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsBaselineFormValidator

    class Meta:
        model = HealthEconomicsBaseline
        fields = "__all__"
