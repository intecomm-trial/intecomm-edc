from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ..admin_site import intecomm_reports_admin
from ..models import Diagnoses


@admin.register(Diagnoses, site=intecomm_reports_admin)
class DiagnosesAdmin(
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    qa_report_list_display_insert_pos = 2
    ordering = ["site", "subject_identifier"]
    list_display = [
        "dashboard",
        "subject_identifier",
        "baseline_date",
        "hiv",
        "htn",
        "dm",
        "hiv_dx_date",
        "htn_dx_date",
        "dm_dx_date",
        "hiv_dx_days",
        "htn_dx_days",
        "dm_dx_days",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        "baseline_date",
        "hiv",
        "htn",
        "dm",
    ]

    readonly_fields = (
        "subject_identifier",
        "baseline_date",
        "hiv",
        "htn",
        "dm",
        "hiv_dx_date",
        "htn_dx_date",
        "dm_dx_date",
        "hiv_dx_days",
        "htn_dx_days",
        "dm_dx_days",
        "site",
    )
