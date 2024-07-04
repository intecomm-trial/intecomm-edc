from django.contrib import admin
from django.db.models import Q, QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import QaReportWithNoteModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_reports_admin
from ..models import VlSummary as VlSummaryModel
from ..vl_summary import VlSummary
from .list_filters import (
    BaselineVlDateListFilter,
    BaselineVlListFilter,
    EndlineVlDateListFilter,
    EndlineVlListFilter,
    LastVlDateListFilter,
    NextVlDateListFilter,
    ScheduleStatusListFilter,
)


@admin.register(VlSummaryModel, site=intecomm_reports_admin)
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
        "baseline_vl",
        "endline_vl",
        "expected",
        "baseline_date",
        "baseline_vl_date",
        "endline_vl_date",
        "last_vl_date",
        "next_vl_date",
        "offschedule_date",
        "offset",
        "created",
    ]

    list_filter = [
        "expected",
        BaselineVlListFilter,
        EndlineVlListFilter,
        ScheduleStatusListFilter,
        "baseline_date",
        BaselineVlDateListFilter,
        EndlineVlDateListFilter,
        LastVlDateListFilter,
        NextVlDateListFilter,
        "offset",
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
        vl_summary = VlSummary(endline_months=9, skip_update_dx=True)
        vl_summary.to_model(model="intecomm_reports.vlsummary")
        qs = super().get_queryset(request)
        return qs.filter((Q(baseline_vl__isnull=True) | Q(endline_vl__isnull=True)))
