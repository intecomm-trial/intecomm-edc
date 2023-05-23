from django import forms
from intecomm_form_validators.subject import HealthEconomicsAssetsFormValidator

from ...models import HealthEconomicsAssets
from ..mixins import CrfModelFormMixin


class HealthEconomicsAssetsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HealthEconomicsAssetsFormValidator

    class Meta:
        model = HealthEconomicsAssets
        fields = "__all__"
