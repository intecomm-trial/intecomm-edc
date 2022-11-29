from django import forms
from edc_rx.modelform_mixins import DrugSupplyNcdModelFormMixin

from intecomm_lists.models import DmTreatments

from ..models import DrugSupplyDm


class DrugSupplyDmForm(DrugSupplyNcdModelFormMixin, forms.ModelForm):
    list_model_cls = DmTreatments
    relation_label = "drugsupplydm"

    class Meta:
        model = DrugSupplyDm
        fields = "__all__"
