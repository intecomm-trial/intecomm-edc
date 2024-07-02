from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import QaReportWithNoteModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import intecomm_reports_admin
from ...models import SubjectsTransferred


@admin.register(SubjectsTransferred, site=intecomm_reports_admin)
class SubjectsTransferredAdmin(
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
        "subject_identifier",
        "last_visit",
        "code",
        "consented",
        "transferred",
        "m",
        "last_seen",
        "offstudy",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        "visit_code",
        "transferred",
    ]

    search_fields = ["subject_identifier"]

    @admin.display(description="M", ordering="months")
    def m(self, obj=None):
        return obj.months

    @admin.display(description="Code", ordering="visit_code")
    def code(self, obj=None):
        return obj.visit_code
