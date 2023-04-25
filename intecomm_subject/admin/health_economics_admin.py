from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin
from ..forms import HealthEconomicsForm
from ..models import HealthEconomics
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomics, site=intecomm_subject_admin)
class HealthEconomicsAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):
    form = HealthEconomicsForm
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Part 1: Education",
            {
                "fields": (
                    "occupation",
                    "education_in_years",
                    "education_certificate",
                    "primary_school",
                    "primary_school_in_years",
                    "secondary_school",
                    "secondary_school_in_years",
                    "higher_education",
                    "higher_education_in_years",
                )
            },
        ),
        (
            "Part 2: Income",
            {"fields": ("welfare", "welfare_other")},
        ),
        (
            "Part 3: Previous Healthcare Expenses: Medication",
            {"fields": ("received_rx_month",)},
        ),
        (
            "Part 3a: Previous Healthcare Expenses: Medication (Diabetes - DM)",
            {
                "fields": (
                    "rx_dm_month",
                    "rx_dm_paid_month",
                    "rx_dm_paid_month_other",
                    "rx_dm_cost_month",
                )
            },
        ),
        (
            "Part 3b: Previous Healthcare Expenses: Medication (Hypertension - HTN)",
            {
                "fields": (
                    "rx_htn_month",
                    "rx_htn_paid_month",
                    "rx_htn_paid_month_other",
                    "rx_htn_cost_month",
                )
            },
        ),
        (
            "Part 3c: Previous Healthcare Expenses: Medication (HIV)",
            {
                "fields": (
                    "rx_hiv_month",
                    "rx_hiv_paid_month",
                    "rx_hiv_paid_month_other",
                    "rx_hiv_cost_month",
                )
            },
        ),
        (
            "Part 3d: Previous Healthcare Expenses: Other Medications",
            {
                "fields": (
                    "rx_other_month",
                    "rx_other_paid_month",
                    "rx_other_paid_month_other",
                    "rx_other_cost_month",
                )
            },
        ),
        (
            "Part 4: Current Visit Healthcare Expenses: Medications",
            {"fields": ("received_rx_today",)},
        ),
        (
            "Part 4a: Current Visit Healthcare Expenses: Medications (Diabetes - DM)",
            {
                "fields": (
                    "rx_dm_today",
                    "rx_dm_paid_today",
                    "rx_dm_paid_today_other",
                    "rx_dm_cost_today",
                )
            },
        ),
        (
            "Part 4b: Current Visit Healthcare Expenses: Medications (Hypertension - HTN)",
            {
                "fields": (
                    "rx_htn_today",
                    "rx_htn_paid_today",
                    "rx_htn_paid_today_other",
                    "rx_htn_cost_today",
                )
            },
        ),
        (
            "Part 4c: Current Visit Healthcare Expenses: Medications (HIV)",
            {
                "fields": (
                    "rx_hiv_today",
                    "rx_hiv_paid_today",
                    "rx_hiv_paid_today_other",
                    "rx_hiv_cost_today",
                )
            },
        ),
        (
            "Part 4d: Current Visit Healthcare Expenses: Other Medications",
            {
                "fields": (
                    "rx_other_today",
                    "rx_other_paid_today",
                    "rx_other_paid_today_other",
                    "rx_other_cost_today",
                )
            },
        ),
        (
            "Part 5: Health Care Financing",
            {
                "fields": (
                    "health_insurance",
                    "health_insurance_cost",
                    "patient_club",
                    "patient_club_cost",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "health_insurance": admin.VERTICAL,
        "higher_education": admin.VERTICAL,
        "patient_club": admin.VERTICAL,
        "primary_school": admin.VERTICAL,
        "received_rx_month": admin.VERTICAL,
        "received_rx_today": admin.VERTICAL,
        "rx_dm_month": admin.VERTICAL,
        "rx_dm_today": admin.VERTICAL,
        "rx_hiv_month": admin.VERTICAL,
        "rx_hiv_today": admin.VERTICAL,
        "rx_htn_month": admin.VERTICAL,
        "rx_htn_today": admin.VERTICAL,
        "rx_other_month": admin.VERTICAL,
        "rx_other_today": admin.VERTICAL,
        "secondary_school": admin.VERTICAL,
        "welfare": admin.VERTICAL,
    }

    filter_horizontal = [
        "rx_dm_paid_month",
        "rx_htn_paid_month",
        "rx_hiv_paid_month",
        "rx_other_paid_month",
        "rx_dm_paid_today",
        "rx_htn_paid_today",
        "rx_hiv_paid_today",
        "rx_other_paid_today",
    ]
