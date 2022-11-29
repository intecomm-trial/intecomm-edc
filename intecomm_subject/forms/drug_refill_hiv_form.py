from django import forms
from intecomm_form_validators.subject import DrugRefillHivFormValidator

from ..models import DrugRefillHiv
from .mixins import CrfModelFormMixin


class DrugRefillHivForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DrugRefillHivFormValidator

    class Meta:
        model = DrugRefillHiv
        fields = "__all__"
