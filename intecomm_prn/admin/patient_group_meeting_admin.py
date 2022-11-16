from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_prn.modeladmin_mixins import PrnModelAdminMixin
from edc_sites.modeladmin_mixins import SiteModelAdminMixin

from ..admin_site import intecomm_prn_admin
from ..forms import PatientGroupMeetingForm
from ..models import PatientGroupMeeting
from .list_filters import PatientGroupApptListFilter as BasePatientGroupApptListFilter


class PatientGroupApptListFilter(BasePatientGroupApptListFilter):
    field_name = "patient_group_appointment__appt_datetime"


@admin.register(PatientGroupMeeting, site=intecomm_prn_admin)
class PatientGroupMeetingAdmin(
    SiteModelAdminMixin,
    PrnModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = PatientGroupMeetingForm

    date_hierarchy = "meeting_datetime"

    show_object_tools = True
    change_list_template: str = "intecomm_prn/admin/patientgroupmeeting_change_list.html"

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "report_datetime",
                    "patient_group_appointment",
                )
            },
        ],
        [
            "Meeting",
            {
                "description": "Complete this section on the day of the meeting",
                "fields": (
                    "meeting_datetime",
                    "patients",
                ),
            },
        ],
        [
            "Notes",
            {"fields": ("notes",)},
        ],
        audit_fieldset_tuple,
    )

    filter_horizontal = ["patients"]

    list_display = (
        "__str__",
        "appt_date",
        "location",
        "patients_in_group",
        "present",
        "absent",
    )

    list_filter = (PatientGroupApptListFilter,)

    search_fields = (
        "patient_group_appointment__patient_group__name",
        "patient_group_appointment__community_care_location__name",
    )

    @admin.display(description="Appt", ordering="patient_group_appointment__appt_datetime")
    def appt_date(self, obj=None):
        return obj.patient_group_appointment.appt_datetime.date()

    @admin.display(description="Location")
    def location(self, obj=None):
        return obj.patient_group_appointment.community_care_location.name.title()

    @admin.display(description="Patients")
    def patients_in_group(self, obj=None):
        count = obj.patient_group_appointment.patient_group.patients.all().count()
        name = obj.patient_group_appointment.patient_group.name
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        return format_html(f'<a href="{url}?={name}">{count}</a>')

    @admin.display(description="Present")
    def present(self, obj=None):
        return obj.patients.all().count()

    @admin.display(description="Absent")
    def absent(self, obj=None):
        total = obj.patient_group_appointment.patient_group.patients.all().count()
        present = obj.patients.all().count()
        return total - present
