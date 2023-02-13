from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import HealthTalkLogFormValidator

from ..models import HealthTalkLog


class HealthTalkLogForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = HealthTalkLogFormValidator

    class Meta:
        model = HealthTalkLog
        fields = "__all__"
