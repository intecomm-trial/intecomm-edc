from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_prn.modeladmin_mixins import PrnModelAdminMixin
from edc_sites.modeladmin_mixins import SiteModelAdminMixin

from ..admin_site import intecomm_prn_admin
from ..forms import PatientGroupAppointmentForm
from ..models import PatientGroupAppointment
from .list_filters import PatientGroupApptListFilter


@admin.register(PatientGroupAppointment, site=intecomm_prn_admin)
class PatientGroupAppointmentAdmin(
    SiteModelAdminMixin,
    PrnModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = PatientGroupAppointmentForm

    autocomplete_fields = ["patient_group", "community_care_location"]

    date_hierarchy = "appt_datetime"

    ordering = ("-appt_datetime",)

    show_object_tools = True
    change_list_template: str = "intecomm_prn/admin/patientgroupappointment_change_list.html"

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "report_datetime",
                    "patient_group",
                    "community_care_location",
                    "appt_datetime",
                    "appt_status",
                )
            },
        ],
        [
            "Notes",
            {"fields": ("notes",)},
        ],
        audit_fieldset_tuple,
    )

    list_display = (
        "title",
        "appt_datetime",
        "appt_status",
        "patient_group_as_link",
        "location_as_link",
    )

    list_filter = (
        PatientGroupApptListFilter,
        "appt_status",
    )

    radio_fields = {"appt_status": admin.VERTICAL}

    search_fields = (
        "community_care_location__name",
        "patient_group__name",
    )

    @admin.display(description="Appointment")
    def title(self, obj=None):
        return f"{obj.patient_group.name}@{obj.community_care_location.name.upper()}"

    @admin.display(description="Patient Group")
    def patient_group_as_link(self, obj=None):
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        search_term = "+".join(obj.patient_group.name.split(" "))
        return format_html(
            f'<a href="{url}?q={search_term}">{obj.patient_group.name.upper()}</a>'
        )

    @admin.display(description="Location")
    def location_as_link(self, obj=None):
        url = reverse("intecomm_prn_admin:intecomm_prn_communitycarelocation_changelist")
        search_term = "+".join(obj.community_care_location.name.split(" "))
        return format_html(
            f'<a href="{url}?q={search_term}">{obj.community_care_location.name.upper()}</a>'
        )
