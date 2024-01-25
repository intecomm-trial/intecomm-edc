from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_randomization.utils import get_object_for_subject
from intecomm_form_validators.subject import LocationUpdateFormValidator

from intecomm_screening.models import PatientLog

from ..models import LocationUpdate


class LocationUpdateForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = LocationUpdateFormValidator

    @property
    def group_identifier(self) -> str:
        obj = PatientLog.objects.get(subject_identifier=self.get_subject_identifier())
        return obj.group_identifier

    def clean(self) -> dict:
        cleaned_data = super().clean()

        rando_obj = get_object_for_subject(
            self.group_identifier, "default", identifier_fld="group_identifier"
        )
        if cleaned_data.get("location") == rando_obj.assignment:
            pass
        return cleaned_data

    class Meta:
        model = LocationUpdate
        fields = "__all__"
