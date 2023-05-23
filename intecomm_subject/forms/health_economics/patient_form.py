from django import forms
from intecomm_form_validators.subject.health_economics import (
    HealthEconomicsPatientFormValidator,
)

from ...models import HealthEconomicsPatient
from ..mixins import CrfModelFormMixin


class HealthEconomicsPatientForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsPatientFormValidator

    class Meta:
        model = HealthEconomicsPatient
        fields = "__all__"
