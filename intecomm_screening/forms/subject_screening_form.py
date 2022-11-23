from django import forms
from edc_form_validators import FormValidatorMixin
from edc_screening.modelform_mixins import AlreadyConsentedFormMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from edc_sites.widgets import SiteField
from intecomm_form_validators import SubjectScreeningFormValidator

from ..models import SubjectScreening


class SubjectScreeningForm(
    AlreadyConsentedFormMixin, SiteModelFormMixin, FormValidatorMixin, forms.ModelForm
):

    form_validator_cls = SubjectScreeningFormValidator

    site = SiteField()

    class Meta:
        model = SubjectScreening
        fields = "__all__"
        labels = {
            "consent_ability": "Is the patient able and willing to give informed consent."
        }
        widgets = {
            "legal_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "familiar_name": forms.TextInput(attrs={"readonly": "readonly"}),
            "initials": forms.TextInput(attrs={"readonly": "readonly"}),
            "age_in_years": forms.TextInput(attrs={"readonly": "readonly"}),
            "hospital_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }
