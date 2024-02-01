from django import forms

from ..models import SubjectConsentTz
from .modelform_mixins import SubjectConsentModelFormMixin


class SubjectConsentTzForm(
    SubjectConsentModelFormMixin,
    forms.ModelForm,
):
    class Meta(SubjectConsentModelFormMixin.Meta):
        model = SubjectConsentTz
