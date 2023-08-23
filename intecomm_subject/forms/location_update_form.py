from django import forms
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_dx_review.form_validator_mixins import ClinicalReviewFollowupFormValidatorMixin
from edc_form_validators import FormValidator
from edc_randomization.utils import get_object_for_subject
from edc_visit_schedule.utils import raise_if_baseline

from intecomm_screening.models import PatientLog

from ..models import LocationUpdate


class LocationUpdateFormValidator(
    ClinicalReviewFollowupFormValidatorMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    def clean(self):
        raise_if_baseline(self.cleaned_data.get("subject_visit"))
        self.validate_other_specify(field="location", other_specify_field="location_other")


class LocationUpdateForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = LocationUpdateFormValidator

    @property
    def group_identifier(self) -> str:
        obj = PatientLog.objects.get(subject_identifier=self.subject_identifier)
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
