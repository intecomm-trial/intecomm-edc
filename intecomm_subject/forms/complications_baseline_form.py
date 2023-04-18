from django import forms
from intecomm_form_validators.subject import ComplicationsBaselineFormValidator

from ..models import ComplicationsBaseline
from .mixins import CrfModelFormMixin


class ComplicationsBaselineForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ComplicationsBaselineFormValidator

    class Meta:
        model = ComplicationsBaseline
        fields = "__all__"
