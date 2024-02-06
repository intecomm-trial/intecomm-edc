from django import forms
from edc_form_validators import FormValidatorMixin
from edc_locator.forms import SubjectLocatorFormValidator
from edc_model_form.mixins import BaseModelFormMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin

__all__ = ["SubjectLocatorForm"]


class SubjectLocatorForm(
    SiteModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    BaseModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = SubjectLocatorFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )
