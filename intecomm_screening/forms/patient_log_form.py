from django import forms
from django.utils.html import format_html
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from intecomm_form_validators import PatientLogFormValidator

from ..models import PatientGroup, PatientLog


class PatientLogForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    form_validator_cls = PatientLogFormValidator

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

    class Meta:
        model = PatientLog
        fields = "__all__"
