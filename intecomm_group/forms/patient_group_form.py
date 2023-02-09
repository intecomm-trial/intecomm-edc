from django import forms
from edc_form_validators import INVALID_ERROR, FormValidator, FormValidatorMixin

from ..models import PatientGroup


class PatientGroupFormValidator(FormValidator):
    def clean(self):
        self.raise_validation_error({"__all__": "This form may not be changed"}, INVALID_ERROR)


class PatientGroupForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PatientGroupFormValidator

    class Meta:
        model = PatientGroup
        fields = "__all__"
