from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators.screening import PatientGroupRandoFormValidator

from ..models import PatientGroupRando


class PatientGroupRandoForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PatientGroupRandoFormValidator

    # TODO: check if any in more than one group

    name = forms.CharField(
        label="Group name",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = PatientGroupRando
        fields = [
            "name",
            "randomized_datetime",
            "randomize_now",
            "confirm_randomize_now",
            "group_identifier",
        ]
