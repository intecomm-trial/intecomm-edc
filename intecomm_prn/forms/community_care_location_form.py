from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.modelform_mixins import SiteModelFormMixin

from ..models import CommunityCareLocation


class CommunityCareLocationForm(
    SiteModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    class Meta:
        model = CommunityCareLocation
        fields = "__all__"
