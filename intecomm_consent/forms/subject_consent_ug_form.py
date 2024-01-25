from django import forms

from ..models import SubjectConsentUg
from .modelform_mixins import SubjectConsentModelFormMixin


class SubjectConsentUgForm(
    SubjectConsentModelFormMixin,
    forms.ModelForm,
):
    class Meta(SubjectConsentModelFormMixin.Meta):
        model = SubjectConsentUg
