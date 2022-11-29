from django import forms
from edc_constants.constants import HIV
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_dx.form_validators import ResultFormValidatorMixin
from edc_form_validators.form_validator import FormValidator

from ..models import Cd4Result


class Cd4ResultFormValidator(ResultFormValidatorMixin, CrfFormValidatorMixin, FormValidator):
    dx = (HIV, "HIV infection")


class Cd4ResultForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = Cd4ResultFormValidator

    class Meta:
        model = Cd4Result
        fields = "__all__"
