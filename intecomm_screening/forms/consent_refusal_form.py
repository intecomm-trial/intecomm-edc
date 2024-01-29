from django import forms
from django.contrib.sites.models import Site
from edc_consent.utils import get_consent_model_cls
from edc_form_validators import FormValidatorMixin
from edc_screening.utils import (
    get_subject_screening_model_cls,
    get_subject_screening_or_raise,
    is_eligible_or_raise,
)
from edc_sites.modelform_mixins import SiteModelFormMixin
from intecomm_form_validators import ConsentRefusalFormValidator
from intecomm_rando.constants import UGANDA

from intecomm_consent.utils import raise_if_subject_consent_exists

from ..models import ConsentRefusal


class ConsentRefusalForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ConsentRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        screening_identifier = self.cleaned_data.get("screening_identifier")
        if subject_screening := get_subject_screening_or_raise(
            screening_identifier, is_modelform=True
        ):
            is_eligible_or_raise(
                screening_identifier=screening_identifier,
                url_name=self.changelist_url,
            )
            raise_if_subject_consent_exists(
                screening_identifier=screening_identifier,
                subject_screening=subject_screening,
                subject_screening_model_cls=get_subject_screening_model_cls(),
                subject_consent_model_cls=get_consent_model_cls(),
                is_modelform=True,
            )
        return cleaned_data

    @property
    def changelist_url(self):
        if Site.objects.get_current().siteprofile.country == UGANDA:
            return "intecomm_screening_admin:intecomm_screening_patientlogug_changlist"
        return "intecomm_screening_admin:intecomm_screening_patientlog_changlist"

    class Meta:
        model = ConsentRefusal
        fields = "__all__"
        help_texts = {"screening_identifier": "(read-only)"}
        widgets = {"screening_identifier": forms.TextInput(attrs={"readonly": "readonly"})}
