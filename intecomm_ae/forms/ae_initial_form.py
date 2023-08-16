from django import forms
from edc_adverse_event.modelform_mixins import AeInitialModelFormMixin

from ..models import AeInitial


class AeInitialForm(AeInitialModelFormMixin, forms.ModelForm):
    class Meta:
        model = AeInitial
        fields = [
            "ae_classification_as_text",
            "ae_description",
            "ae_awareness_date",
            "ae_start_date",
            "ae_grade",
            "ae_treatment",
        ]
        help_texts = {"subject_identifier": "(read-only)", "action_identifier": "(read-only)"}
        widgets = {
            "subject_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
            "action_identifier": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    def validate_sae_and_grade(self):
        pass
