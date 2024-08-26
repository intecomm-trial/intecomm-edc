from django.contrib import admin
from django.db.models import QuerySet
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_reports_admin
from ..models import MissingVlDrawDates
from ..vl import get_missing_drawn_dates_df
from .list_filters import ScheduleStatusListFilter


@admin.register(MissingVlDrawDates, site=intecomm_reports_admin)
class MissingVlDrawDatesAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ["site", "subject_identifier"]

    list_display = [
        "dashboard",
        "subject_identifier",
        "baseline_date",
        "visit_code",
        "visit_date",
        "vl",
        "site",
        "created",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        "visit_code",
    ]

    search_fields = ["id", "subject_identifier"]

    def get_queryset(self, request) -> QuerySet:
        get_missing_drawn_dates_df(model="intecomm_reports.missingvldrawdates")
        return super().get_queryset(request)
