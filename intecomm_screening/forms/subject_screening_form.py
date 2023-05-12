from __future__ import annotations

from django import forms
from django.urls import reverse
from edc_dashboard import url_names
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

    def already_consented_validation_url(self, cleaned_data: dict | None = None) -> str:
        if self.instance.patient_log.group_identifier:
            url_name = url_names.get("subject_dashboard_url")
            url = reverse(
                url_name,
                kwargs={"subject_identifier": self.instance.subject_identifier},
            )
        else:
            url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
            url = f"{url}?q={self.instance.subject_identifier}"
        return url

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
