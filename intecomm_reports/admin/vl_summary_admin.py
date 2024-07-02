from django.contrib import admin
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import QaReportWithNoteModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from intecomm_reports.admin.list_filters import (
    BaselineVlListFilter,
    EndlineVlListFilter,
    ScheduleStatusListFilter,
)
from intecomm_reports.admin_site import intecomm_reports_admin
from intecomm_reports.models import VlSummary
from intecomm_reports.utils import vl_summary_to_table


@admin.register(VlSummary, site=intecomm_reports_admin)
class VlSummaryAdmin(
    QaReportWithNoteModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    qa_report_list_display_insert_pos = 2
    ordering = ["site", "subject_identifier"]
    list_display = [
        "dashboard",
        "subject",
        "baseline_date",
        "baseline_vl",
        "baseline_vl_date",
        "endline_vl",
        "endline_vl_date",
        "created",
    ]

    list_filter = [
        BaselineVlListFilter,
        EndlineVlListFilter,
        ScheduleStatusListFilter,
        "baseline_date",
        "baseline_vl_date",
        "endline_vl_date",
    ]

    search_fields = ["subject_identifier"]

    @admin.display(description="Subject", ordering="subject_identifier")
    def subject(self, obj):
        url = reverse("intecomm_reports_admin:intecomm_reports_vl_changelist")
        context = dict(url=url, subject_identifier=obj.subject_identifier)
        return render_to_string(
            "intecomm_reports/columns/vl_subject_identifier.html", context=context
        )

    def get_queryset(self, request) -> QuerySet:
        vl_summary_to_table()
        return super().get_queryset(request)
