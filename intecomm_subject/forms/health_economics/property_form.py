from django import forms
from intecomm_form_validators.subject.health_economics import (
    HealthEconomicsPropertyFormValidator,
)

from ...models import HealthEconomicsProperty
from ..mixins import CrfModelFormMixin


class HealthEconomicsPropertyForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsPropertyFormValidator

    class Meta:
        model = HealthEconomicsProperty
        fields = "__all__"
