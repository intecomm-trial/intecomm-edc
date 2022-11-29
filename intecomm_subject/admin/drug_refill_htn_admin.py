from django.contrib import admin
from edc_model_admin.mixins import TabularInlineMixin
from edc_rx.modeladmin_mixins import DrugRefillAdminMixin, DrugSupplyInlineMixin

from ..admin_site import intecomm_subject_admin
from ..forms import DrugRefillHtnForm, DrugSupplyHtnForm
from ..models import DrugRefillHtn, DrugSupplyHtn
from .modeladmin_mixins import CrfModelAdmin


class DrugSupplyHtnInline(DrugSupplyInlineMixin, TabularInlineMixin, admin.TabularInline):
    model = DrugSupplyHtn
    form = DrugSupplyHtnForm


@admin.register(DrugRefillHtn, site=intecomm_subject_admin)
class DrugRefillHtnAdmin(DrugRefillAdminMixin, CrfModelAdmin):
    form = DrugRefillHtnForm
    inlines = [DrugSupplyHtnInline]
