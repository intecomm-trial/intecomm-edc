from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_model_fields.widgets import SliderWidget
from intecomm_form_validators.subject import HivMedicationAdherenceFormValidator

from ..models import HivMedicationAdherence


class HivMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HivMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual score for your HIV medication",
        widget=SliderWidget(attrs={"min": 0, "max": 100}),
    )

    class Meta:
        model = HivMedicationAdherence
        fields = "__all__"
        labels = {
            "last_missed_pill": (
                "When was the last time you missed taking your HIV medication?"
            ),
            "missed_pill_reason": (
                "If your HIV medication was not taken, select a reason or reasons"
            ),
        }
