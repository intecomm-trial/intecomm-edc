from django import forms
from edc_form_validators import FormValidator

from ..models import Icecapa
from .mixins import CrfModelFormMixin


class IcecapaFormValidator(FormValidator):
    pass


class IcecapaForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = IcecapaFormValidator

    class Meta:
        model = Icecapa
        fields = "__all__"
