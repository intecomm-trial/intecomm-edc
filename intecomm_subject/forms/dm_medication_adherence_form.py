from django import forms
from edc_model.widgets import SliderWidget
from intecomm_form_validators.subject import DmMedicationAdherenceFormValidator

from ..models import DmMedicationAdherence
from .mixins import CrfModelFormMixin


class DmMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DmMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual score for your diabetes medication",
        widget=SliderWidget(attrs={"min": 0, "max": 100}),
    )

    class Meta:
        model = DmMedicationAdherence
        fields = "__all__"
        labels = {
            "last_missed_pill": (
                "When was the last time you missed taking your diabetes medication?"
            ),
            "missed_pill_reason": (
                "If your diabetes medication was missed, select a reason or reasons"
            ),
        }
