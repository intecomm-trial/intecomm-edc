from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.utils import get_subject_screening_or_raise, is_eligible_or_raise
from intecomm_form_validators import ConsentRefusalFormValidator

from intecomm_consent.utils import raise_if_subject_consent_exists

from ..models import ConsentRefusal


class ConsentRefusalForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ConsentRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        screening_identifier = self.cleaned_data.get("screening_identifier")
        if get_subject_screening_or_raise(screening_identifier, is_modelform=True):
            is_eligible_or_raise(
                screening_identifier=screening_identifier,
                url_name="intecomm_screening_admin:intecomm_screening_patientlog_changlist",
            )
            raise_if_subject_consent_exists(
                screening_identifier=screening_identifier, is_modelform=True
            )
        return cleaned_data

    class Meta:
        model = ConsentRefusal
        fields = "__all__"
        help_texts = {"screening_identifier": "(read-only)"}
        widgets = {"screening_identifier": forms.TextInput(attrs={"readonly": "readonly"})}
