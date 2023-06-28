from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import ConsentRefusalFormValidator

from intecomm_consent.utils import validate_not_already_consented

from ..models import ConsentRefusal
from ..utils import (
    validate_is_eligible,
    validate_not_already_refused_consent,
    validate_not_screened_despite_unwilling_to_screen,
)


class RefusalFormMixin:
    def clean(self):
        cleaned_data = super().clean()
        subject_screening = cleaned_data.get("subject_screening")
        if subject_screening:
            validate_not_screened_despite_unwilling_to_screen(
                subject_screening=subject_screening
            )
            validate_is_eligible(subject_screening=subject_screening)
            validate_not_already_refused_consent(subject_screening=subject_screening)
            validate_not_already_consented(subject_screening=subject_screening)

        return cleaned_data


class ConsentRefusalForm(RefusalFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ConsentRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = ConsentRefusal
        fields = "__all__"
        help_texts = {"subject_screening": "(read-only)"}
        widgets = {"subject_screening": forms.TextInput(attrs={"readonly": "readonly"})}
