from django.contrib import admin
from django.db.models import Q, QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ..vl import VlSummary
from .list_filters import (
    BaselineVlDateListFilter,
    BaselineVlListFilter,
    EndlineVlDateListFilter,
    EndlineVlListFilter,
    LastVlDateListFilter,
    NextVlDateListFilter,
    ScheduleStatusListFilter,
)


class VlSummaryModelAdminMixin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
):
    report_model: str = None
    endline_months: int = None

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
        vl_summary = VlSummary(endline_months=self.endline_months, skip_update_dx=True)
        vl_summary.to_model(model=self.report_model)
        qs = super().get_queryset(request)
        return qs.filter((Q(baseline_vl__isnull=True) | Q(endline_vl__isnull=True)))
