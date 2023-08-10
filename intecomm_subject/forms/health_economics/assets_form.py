from django import forms
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_he.form_validators import HealthEconomicsAssetsFormValidator

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

    class Meta:
        model = HealthEconomicsAssets
        fields = "__all__"
