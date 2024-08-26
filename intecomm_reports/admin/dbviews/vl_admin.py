from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ...admin_site import intecomm_reports_admin
from ...models import Vl
from ..list_filters import ScheduleStatusListFilter, VlDateListFilter, VlListFilter


@admin.register(Vl, site=intecomm_reports_admin)
class VlAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    include_note_column = False
    ordering = ["site", "subject_identifier"]

    list_display = [
        "dashboard",
        "subject",
        "vl_value",
        "baseline_date",
        "vl_date",
        "m",
        "site",
        "created",
    ]

    list_filter = [VlListFilter, VlDateListFilter, ScheduleStatusListFilter]

    search_fields = ["id", "subject_identifier", "vl_value"]

    @admin.display(description="Subject", ordering="subject_identifier")
    def subject(self, obj):
        url = reverse("intecomm_reports_admin:intecomm_reports_vl_changelist")
        context = dict(url=url, subject_identifier=obj.subject_identifier)
        return render_to_string(
            "intecomm_reports/columns/vl_subject_identifier.html", context=context
        )
