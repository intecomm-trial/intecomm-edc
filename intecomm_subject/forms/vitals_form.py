from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from intecomm_form_validators.subject import VitalsFormValidator

from ..models import Vitals


class VitalsForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = VitalsFormValidator

    class Meta:
        model = Vitals
        fields = "__all__"
