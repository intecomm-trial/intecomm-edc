from django import forms
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_he.form_validators import HealthEconomicsPropertyFormValidator

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

    class Meta:
        model = HealthEconomicsProperty
        fields = "__all__"
