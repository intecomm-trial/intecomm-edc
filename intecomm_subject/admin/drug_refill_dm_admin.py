from django.contrib import admin
from django.utils.safestring import mark_safe
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin, TabularInlineMixin

from ..admin_site import intecomm_subject_admin

# from ..forms import DrugRefillDmForm
from ..models import DrugRefillDm, DrugSupplyDm
from .modeladmin_mixins import CrfModelAdminMixin, DrugSupplyInlineMixin

# from intecomm_subject.forms import DrugSupplyDmForm


class DrugSupplyDmInline(DrugSupplyInlineMixin, TabularInlineMixin, admin.TabularInline):

    model = DrugSupplyDm
    # form = DrugSupplyDmForm
    min_num = 1
    insert_after = "return_in_days"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


@admin.register(DrugRefillDm, site=intecomm_subject_admin)
class DrugRefillDmAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):
    # form = DrugRefillDmForm

    additional_instructions = mark_safe(
        '<span style="color:orange">Note: Medications CRF must be completed first.</span>'
    )

    inlines = [DrugSupplyDmInline]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diabetes Drug Refill Today",
            {
                "fields": (
                    "rx",
                    "rx_other",
                    "rx_modified",
                    "modifications",
                    "modifications_other",
                    "modifications_reason",
                    "modifications_reason_other",
                    "return_in_days",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )
    filter_horizontal = ["rx", "modifications", "modifications_reason"]

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "rx_modified": admin.VERTICAL,
    }
