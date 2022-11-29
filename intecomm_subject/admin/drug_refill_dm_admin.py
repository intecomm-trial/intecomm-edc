from django.contrib import admin
from edc_model_admin.mixins import TabularInlineMixin
from edc_rx.modeladmin_mixins import DrugRefillAdminMixin, DrugSupplyInlineMixin

from ..admin_site import intecomm_subject_admin
from ..forms import DrugRefillDmForm, DrugSupplyDmForm
from ..models import DrugRefillDm, DrugSupplyDm
from .modeladmin_mixins import CrfModelAdmin


class DrugSupplyDmInline(DrugSupplyInlineMixin, TabularInlineMixin, admin.TabularInline):
    model = DrugSupplyDm
    form = DrugSupplyDmForm


@admin.register(DrugRefillDm, site=intecomm_subject_admin)
class DrugRefillDmAdmin(DrugRefillAdminMixin, CrfModelAdmin):
    form = DrugRefillDmForm
    inlines = [DrugSupplyDmInline]
