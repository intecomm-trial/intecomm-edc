from django import forms
from edc_adverse_event.modelform_mixins import AeInitialModelFormMixin

from ..models import AeInitial


class AeInitialForm(AeInitialModelFormMixin, forms.ModelForm):
    class Meta(AeInitialModelFormMixin.Meta):
        model = AeInitial
        fields = [
            "ae_classification_as_text",
            "ae_description",
            "ae_awareness_date",
            "ae_start_date",
            "ae_grade",
            "ae_treatment",
        ]
