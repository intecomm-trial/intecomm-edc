from django import forms
from intecomm_form_validators.subject.health_economics import (
    HealthEconomicsIncomeFormValidator,
)

from ...models import HealthEconomicsIncome
from ..mixins import CrfModelFormMixin
from .modelform_mixins import HealthEconomicsModelFormMixin


class HealthEconomicsIncomeForm(
    HealthEconomicsModelFormMixin, CrfModelFormMixin, forms.ModelForm
):
    form_validator_cls = HealthEconomicsIncomeFormValidator

    class Meta:
        model = HealthEconomicsIncome
        fields = "__all__"
