from django import forms
from intecomm_form_validators.subject.health_economics import (
    HealthEconomicsPropertyFormValidator,
)

from ...models import HealthEconomicsProperty
from ..mixins import CrfModelFormMixin
from .modelform_mixins import HealthEconomicsModelFormMixin


class HealthEconomicsPropertyForm(
    HealthEconomicsModelFormMixin, CrfModelFormMixin, forms.ModelForm
):
    form_validator_cls = HealthEconomicsPropertyFormValidator

    class Meta:
        model = HealthEconomicsProperty
        fields = "__all__"
