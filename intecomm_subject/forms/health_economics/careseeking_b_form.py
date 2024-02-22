from django import forms
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin

from ...models import CareseekingB
from ..mixins import CrfModelFormMixin


class CareseekingBForm(
    CrfSingletonModelFormMixin,
    CrfModelFormMixin,
    forms.ModelForm,
):
    form_validator_cls = None

    class Meta:
        model = CareseekingB
        fields = "__all__"
