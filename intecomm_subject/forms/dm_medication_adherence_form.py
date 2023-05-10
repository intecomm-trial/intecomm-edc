from django import forms
from edc_model.widgets import SliderWidget
from intecomm_form_validators.subject import DmMedicationAdherenceFormValidator

from ..models import DmMedicationAdherence
from .mixins import CrfModelFormMixin


class DmMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = DmMedicationAdherence
        fields = "__all__"
