from django import forms
from edc_form_validators import FormValidator

from ..models import FamilyHistory
from .mixins import CrfModelFormMixin


class FamilyHistoryFormValidator(FormValidator):
    pass


class FamilyHistoryForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = FamilyHistoryFormValidator

    class Meta:
        model = FamilyHistory
        fields = "__all__"
