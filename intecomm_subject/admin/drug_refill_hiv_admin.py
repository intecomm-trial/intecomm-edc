from django.contrib import admin
from edc_model_admin.mixins import TabularInlineMixin
from edc_rx.modeladmin_mixins import DrugRefillAdminMixin, DrugSupplyInlineMixin

from ..admin_site import intecomm_subject_admin
from ..forms import DrugRefillHivForm, DrugSupplyHivForm
from ..models import DrugRefillHiv, DrugSupplyHiv
from .modeladmin_mixins import CrfModelAdmin


class DrugSupplyHivInline(DrugSupplyInlineMixin, TabularInlineMixin, admin.TabularInline):
    model = DrugSupplyHiv
    form = DrugSupplyHivForm


@admin.register(DrugRefillHiv, site=intecomm_subject_admin)
class DrugRefillHivAdmin(DrugRefillAdminMixin, CrfModelAdmin):
    form = DrugRefillHivForm
    autocomplete_fields = ["rx"]

    filter_horizontal = ["modifications", "modifications_reason"]
