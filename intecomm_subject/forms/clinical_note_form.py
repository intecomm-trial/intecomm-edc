from django import forms
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from edc_visit_schedule.utils import raise_if_baseline

from ..models import ClinicalNote


class ClinicalNoteFormValidator(CrfFormValidatorMixin, FormValidator):
    def clean(self):
        raise_if_baseline(self.cleaned_data.get("subject_visit"))


class ClinicalNoteForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ClinicalNoteFormValidator

    class Meta:
        model = ClinicalNote
        fields = "__all__"
