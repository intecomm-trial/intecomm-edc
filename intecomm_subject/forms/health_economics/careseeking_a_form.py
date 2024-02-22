from django import forms
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_form_validators import FormValidator

from ...models import CareseekingA
from ..mixins import CrfModelFormMixin


class CareseekingAFormValidator(FormValidator):
    def clean(self) -> None:
        pass


class CareseekingAForm(
    CrfSingletonModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = CareseekingAFormValidator

    class Meta:
        model = CareseekingA
        fields = "__all__"
