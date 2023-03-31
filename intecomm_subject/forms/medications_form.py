from django import forms
from intecomm_form_validators.subject import MedicationsFormValidator

from ..models import Medications
from .mixins import CrfModelFormMixin


class MedicationsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = MedicationsFormValidator

    class Meta:
        model = Medications
        fields = "__all__"
