from django import forms
from edc_constants.constants import YES
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import ConsentRefusalFormValidator

from intecomm_consent.utils import raise_if_subject_consent_exists

from ..models import ConsentRefusal
from ..utils import raise_if_consent_refusal_exists, raise_if_not_eligible


class ConsentRefusalForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ConsentRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        if subject_screening := cleaned_data.get("subject_screening"):
            raise_if_consent_refusal_exists(
                screening_identifier=subject_screening.screening_identifier, is_modelform=True
            )
            raise_if_subject_consent_exists(
                subject_screening=subject_screening, is_modelform=True
            )
            raise_if_not_eligible(subject_screening=subject_screening)
            if subject_screening.patient_log.willing_to_screen == YES:
                raise forms.ValidationError(
                    f"Subject is willing to screen. See {subject_screening._meta.verbose_name}"
                )
        return cleaned_data

    class Meta:
        model = ConsentRefusal
        fields = "__all__"
        help_texts = {"subject_screening": "(read-only)"}
        widgets = {"subject_screening": forms.TextInput(attrs={"readonly": "readonly"})}
