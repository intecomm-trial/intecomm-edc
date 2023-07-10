from django.contrib import admin
from edc_model_admin.mixins import InlineHideOriginalObjectNameMixin, TabularInlineMixin
from edc_rx.modeladmin_mixins import DrugRefillAdminMixin, DrugSupplyInlineMixin

from ..admin_site import intecomm_subject_admin
from ..forms import DrugRefillHtnForm, DrugSupplyHtnForm
from ..models import DrugRefillHtn, DrugSupplyHtn
from .modeladmin_mixins import CrfModelAdmin


class DrugSupplyHtnInline(DrugSupplyInlineMixin, TabularInlineMixin, admin.TabularInline):
    model = DrugSupplyHtn
    form = DrugSupplyHtnForm


@admin.register(DrugRefillHtn, site=intecomm_subject_admin)
class DrugRefillHtnAdmin(
    DrugRefillAdminMixin,
    InlineHideOriginalObjectNameMixin,
    CrfModelAdmin,
):
    form = DrugRefillHtnForm
    inlines = [DrugSupplyHtnInline]

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.insert_before_fieldset = self.insert_before_fieldset
        return formset
