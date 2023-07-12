from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_model_admin.mixins import InlineHideOriginalObjectNameMixin, TabularInlineMixin
from edc_rx.modeladmin_mixins import DrugRefillAdminMixin, DrugSupplyInlineMixin

from ..admin_site import intecomm_subject_admin
from ..forms import DrugRefillHivForm, DrugSupplyHivForm
from ..models import DrugRefillHiv, DrugSupplyHiv
from .modeladmin_mixins import CrfModelAdmin


class DrugSupplyHivInline(DrugSupplyInlineMixin, TabularInlineMixin, admin.TabularInline):
    model = DrugSupplyHiv
    form = DrugSupplyHivForm


@admin.register(DrugRefillHiv, site=intecomm_subject_admin)
class DrugRefillHivAdmin(
    DrugRefillAdminMixin,
    InlineHideOriginalObjectNameMixin,
    CrfModelAdmin,
):
    form = DrugRefillHivForm
    autocomplete_fields = ["rx"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Refill Information",
            {
                "fields": (
                    "rx",
                    "rx_other",
                    "rx_modified",
                    "modifications",
                    "modifications_other",
                    "modifications_reason",
                    "modifications_reason_other",
                )
            },
        ),
        (
            "Drug Supply: HIV",
            {
                "fields": (
                    "rx_days",
                    "clinic_days",
                    "club_days",
                    "purchased_days",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ["modifications", "modifications_reason"]
