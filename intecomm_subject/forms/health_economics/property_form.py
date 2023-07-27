from django import forms
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from intecomm_form_validators.subject.health_economics import (
    HealthEconomicsPropertyFormValidator,
)

from ...models import HealthEconomicsProperty
from ..mixins import CrfModelFormMixin
from .modelform_mixins import HealthEconomicsModelFormMixin


class HealthEconomicsPropertyForm(
    CrfSingletonModelFormMixin,
    HealthEconomicsModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HealthEconomicsPropertyFormValidator

    def clean(self):
        self.raise_if_singleton_exists()
        return super().clean()

    class Meta:
        model = HealthEconomicsProperty
        fields = "__all__"
