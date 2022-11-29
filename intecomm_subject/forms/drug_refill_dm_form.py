from django import forms
from intecomm_form_validators.subject import DrugRefillDmFormValidator

from ..models import DrugRefillDm
from .mixins import CrfModelFormMixin


class DrugRefillDmForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DrugRefillDmFormValidator

    class Meta:
        model = DrugRefillDm
        fields = "__all__"
