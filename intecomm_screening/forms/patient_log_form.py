from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from edc_sites.widgets import SiteField

from ..models import PatientLog


class PatientLogForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):
    site = SiteField(label="Health facility")

    class Meta:
        model = PatientLog
        fields = "__all__"
