from django import forms
from edc_model.widgets import SliderWidget
from intecomm_form_validators.subject import HtnMedicationAdherenceFormValidator

from ..models import HtnMedicationAdherence
from .mixins import CrfModelFormMixin


class HtnMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HtnMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = HtnMedicationAdherence
        fields = "__all__"
