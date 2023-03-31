from django import forms
from intecomm_form_validators.subject import OtherBaselineDataFormValidator

from ..models import OtherBaselineData
from .mixins import CrfModelFormMixin


class OtherBaselineDataForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = OtherBaselineDataFormValidator

    class Meta:
        model = OtherBaselineData
        fields = "__all__"
