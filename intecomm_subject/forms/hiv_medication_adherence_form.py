from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_model_fields.widgets import SliderWidget
from intecomm_form_validators.subject import HivMedicationAdherenceFormValidator

from ..models import HivMedicationAdherence


class HivMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HivMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = HivMedicationAdherence
        fields = "__all__"
