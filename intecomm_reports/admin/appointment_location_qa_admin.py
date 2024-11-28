from django.contrib import admin
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from edc_appointment.models import Appointment
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_pdutils.utils import refresh_model_from_dataframe
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from intecomm_analytics.dataframes import get_appointment_location_qa_df

from ..admin_site import intecomm_reports_admin
from ..models import AppointmentLocationQa


@admin.register(AppointmentLocationQa, site=intecomm_reports_admin)
class AppointmentLocationQaAdmin(
    QaReportModelAdminMixin,
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
        "visit_code",
        "visit_code_sequence",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        "visit_code",
        "visit_code_sequence",
    ]

    readonly_fields = (
        "subject_identifier",
        "visit_code",
        "visit_code_sequence",
        "site",
    )

    search_fields = ["subject_identifier"]

    def get_queryset(self, request) -> QuerySet:
        df = get_appointment_location_qa_df()
        refresh_model_from_dataframe(df, model_cls=AppointmentLocationQa)
        qs = super().get_queryset(request)
        return qs

    def dashboard(self, obj=None, label=None) -> str:
        appointment = Appointment.objects.get(
            subject_identifier=obj.subject_identifier,
            visit_code=obj.visit_code,
            visit_code_sequence=obj.visit_code_sequence,
        )

        dashboard_url = reverse(
            f"edc_appointment_admin:"
            f"{Appointment._meta.label_lower.replace('.', '_')}_change",
            args=(appointment.id,),
        )
        dashboard_url = (
            f"{dashboard_url}?next={self.admin_site.name}:"
            f"{self.model._meta.label_lower.replace('.', '_')}_changelist"
        )
        title = _(f"Change {Appointment._meta.verbose_name}")
        label = _(f"Change {Appointment._meta.verbose_name}")

        context = dict(title=title, url=dashboard_url, label=label)
        return render_to_string("dashboard_button.html", context=context)
