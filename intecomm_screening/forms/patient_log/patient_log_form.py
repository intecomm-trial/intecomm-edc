import re

from django import forms
from django.utils.html import format_html
from edc_constants.constants import UUID_PATTERN
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from intecomm_form_validators import PatientLogFormValidator

from ...models import PatientGroup, PatientLog


class PatientLogFormMixin:
    def clean(self) -> dict:
        if self.instance.id:
            qs = PatientGroup.objects.filter(patients__in=[self.instance])
            if qs.count() > 0:
                raise forms.ValidationError(
                    format_html(
                        "Changes not allowed. Patient is already in group <A href="
                        f"{qs[0].get_absolute_url()}>{qs[0].name}</A>."
                    )
                )
        return super().clean()

    def get_initial_for_field(self, field, field_name):
        """Set existing data value to None if UUID.

        Required for forms that were saved when the
        name fields were hidden by mistake.
        """
        value = super().get_initial_for_field(field, field_name)
        if value and field_name in ["legal_name", "familiar_name"]:
            if re.match(UUID_PATTERN, value):
                value = None
        return value


class PatientLogForm(
    PatientLogFormMixin,
    AlreadyConsentedFormMixin,
    SiteModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = PatientLogFormValidator

    class Meta:
        model = PatientLog
        fields = "__all__"
