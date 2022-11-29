from django import forms
from edc_rx.modelform_mixins import DrugSupplyNcdModelFormMixin

from intecomm_lists.models import HtnTreatments

from ..models import DrugSupplyHtn


class DrugSupplyHtnForm(DrugSupplyNcdModelFormMixin, forms.ModelForm):
    list_model_cls = HtnTreatments
    relation_label = "drugsupplyhtn"

    class Meta:
        model = DrugSupplyHtn
        fields = "__all__"
