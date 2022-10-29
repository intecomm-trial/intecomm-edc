from django import forms
from edc_form_validators import FormValidatorMixin

from ..models import PatientGroup


class PatientGroupForm(FormValidatorMixin, forms.ModelForm):
    class Meta:
        model = PatientGroup
        fields = "__all__"
