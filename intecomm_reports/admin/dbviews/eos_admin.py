from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ...admin_site import intecomm_reports_admin
from ...models import Eos


@admin.register(Eos, site=intecomm_reports_admin)
class EosAdmin(
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
        "visit",
        "visit_date",
        "offstudy_date",
        "offstudy_reason",
        "m",
        "schedule_status",
        "site",
        "created",
    ]

    list_filter = [
        "visit_datetime",
        "offstudy_datetime",
        "schedule_status",
        "offstudy_reason",
        "visit_code",
        "visit_code_sequence",
        "m",
    ]

    search_fields = ["subject_identifier"]

    @admin.display(description="Subject", ordering="subject_identifier")
    def subject(self, obj):
        return obj.subject_identifier

    @admin.display(description="Last visit", ordering="visit_code")
    def visit(self, obj):
        return f"{obj.visit_code}.{obj.visit_code_sequence}"

    @admin.display(description="Visit date", ordering="visit_datetime")
    def visit_date(self, obj):
        if obj.visit_datetime:
            return obj.visit_datetime.date()

        return None

    @admin.display(description="Offstudy date", ordering="offstudy_datetime")
    def offstudy_date(self, obj):
        if obj.offstudy_datetime:
            return obj.offstudy_datetime.date()
        return None

    @admin.display(description="Months", ordering="~m")
    def months(self, obj):
        return abs(obj.m)
