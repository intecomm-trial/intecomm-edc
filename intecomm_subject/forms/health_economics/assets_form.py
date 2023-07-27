from django import forms
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from intecomm_form_validators.subject import HealthEconomicsAssetsFormValidator

from ...models import HealthEconomicsAssets
from ..mixins import CrfModelFormMixin
from .modelform_mixins import HealthEconomicsModelFormMixin


class HealthEconomicsAssetsForm(
    CrfSingletonModelFormMixin,
    HealthEconomicsModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HealthEconomicsAssetsFormValidator

    def clean(self):
        self.raise_if_singleton_exists()
        return super().clean()

    class Meta:
        model = HealthEconomicsAssets
        fields = "__all__"
