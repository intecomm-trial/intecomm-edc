from django import forms
from edc_constants.constants import HIV
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_dx.form_validators import ResultFormValidatorMixin
from edc_form_validators.form_validator import FormValidator

from ..models import ViralLoadResult


class ViralLoadResultFormValidator(
    ResultFormValidatorMixin, CrfFormValidatorMixin, FormValidator
):
    dx = (HIV, "HIV infection")


class ViralLoadResultForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ViralLoadResultFormValidator

    class Meta:
        model = ViralLoadResult
        fields = "__all__"
