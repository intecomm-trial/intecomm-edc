from django import forms
from edc_model.widgets import SliderWidget
from intecomm_form_validators.subject import HtnMedicationAdherenceFormValidator

from ..models import HtnMedicationAdherence
from .mixins import CrfModelFormMixin


class HtnMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HtnMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual score for your hypertension medication",
        widget=SliderWidget(attrs={"min": 0, "max": 100}),
    )

    class Meta:
        model = HtnMedicationAdherence
        fields = "__all__"
        labels = {
            "last_missed_pill": (
                "When was the last time you missed taking your hypertension medication?"
            ),
            "missed_pill_reason": (
                "If your hypertension medication was missed, select a reason or reasons"
            ),
        }
