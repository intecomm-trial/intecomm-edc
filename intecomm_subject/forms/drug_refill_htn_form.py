from django import forms
from intecomm_form_validators.subject import DrugRefillHtnFormValidator

from ..models import DrugRefillHtn
from .mixins import CrfModelFormMixin


class DrugRefillHtnForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DrugRefillHtnFormValidator

    class Meta:
        model = DrugRefillHtn
        fields = "__all__"
