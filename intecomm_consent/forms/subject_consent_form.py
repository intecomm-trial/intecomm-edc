from django import forms

from ..models import SubjectConsent
from .modelform_mixins import SubjectConsentModelFormMixin


class SubjectConsentForm(
    SubjectConsentModelFormMixin,
    forms.ModelForm,
):
    class Meta(SubjectConsentModelFormMixin.Meta):
        model = SubjectConsent
