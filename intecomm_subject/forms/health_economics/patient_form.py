from django import forms
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from intecomm_form_validators.subject.health_economics import (
    HealthEconomicsPatientFormValidator,
)

from ...models import HealthEconomicsPatient
from ..mixins import CrfModelFormMixin
from .modelform_mixins import HealthEconomicsModelFormMixin


class HealthEconomicsPatientForm(
    CrfSingletonModelFormMixin,
    HealthEconomicsModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HealthEconomicsPatientFormValidator

    def clean(self):
        self.raise_if_singleton_exists()
        return super().clean()

    class Meta:
        model = HealthEconomicsPatient
        fields = "__all__"
