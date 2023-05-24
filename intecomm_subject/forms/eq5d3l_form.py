from django import forms
from edc_form_validators import FormValidator
from edc_model_fields.widgets import SliderWidget

from ..models import Eq5d3l
from .mixins import CrfModelFormMixin


class Eq5d3lFormValidator(FormValidator):
    pass


class Eq5d3lForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = Eq5d3lFormValidator

    health_today_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = Eq5d3l
        fields = "__all__"
