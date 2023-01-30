import inflect
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import COMPLETE, NEW
from intecomm_form_validators import RECRUITING
from intecomm_rando.constants import COMM_INTERVENTION
from intecomm_rando.models import RandomizationList

from intecomm_screening.admin.modeladmin_mixins import BaseModelAdminMixin

from ..admin_site import intecomm_group_admin
from ..exceptions import PatientGroupNotRandomized
from ..forms import PatientGroupForm
from ..models import PatientGroup
from ..utils import get_assignment_description_for_patient_group

p = inflect.engine()


@admin.register(PatientGroup, site=intecomm_group_admin)
class PatientGroupAdmin(BaseModelAdminMixin):

    """Modeladmin for patient groups in follow-up or dissolved.

    See `get_queryset`"""

    form = PatientGroupForm

    show_object_tools = True
    change_list_template: str = "intecomm_group/admin/patientgroup_change_list.html"
    show_save_next = False
    show_cancel = True

    fieldsets = (
        (
            None,
            {"fields": ("report_datetime", "name", "status", "notes")},
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "__str__",
        "group_identifier",
        "randomized_date",
        "status",
        "to_subjects",
        "arm",
        "meetings",
        "opened",
        "user_created",
        "created",
    )

    list_filter = (
        "status",
        "randomized",
        "report_datetime",
        "randomized_datetime",
    )

    search_fields = (
        "name",
        "group_identifier",
        "patients__legal_name__exact",
        "patients__familiar_name__exact",
        "patients__initials__iexact",
    )

    radio_fields = {
        "status": admin.VERTICAL,
    }

    readonly_fields = (
        "report_datetime",
        "name",
        "status",
        "randomized",
        "randomized_datetime",
    )

    @admin.display(description="Randomized", ordering="randomized_datetime")
    def randomized_date(self, obj=None):
        try:
            return obj.randomized_datetime.date()
        except AttributeError:
            return None

    @admin.display(description="Arm")
    def arm(self, obj=None):
        try:
            arm_as_str = get_assignment_description_for_patient_group(obj.group_identifier)
        except PatientGroupNotRandomized:
            link = None
        else:
            url = reverse("intecomm_group_admin:intecomm_group_patientgroup_changelist")
            url = f"{url}?q={obj.name}"
            link = format_html(
                f'<a title="Go to group followup" href="{url}">{arm_as_str}</a>'
            )
        return link

    @admin.display(description="Opened", ordering="report_datetime")
    def opened(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="Meetings")
    def meetings(self, obj=None):
        name = "+".join(obj.name.split(" "))
        url = reverse("intecomm_group_admin:intecomm_group_patientgroupmeeting_changelist")
        url = f"{url}?q={name}"
        return format_html(f'<a href="{url}">Meetings</a>')

    @admin.display(description="Patients")
    def to_subjects(self, obj=None):
        if (
            RandomizationList.objects.get(group_identifier=obj.group_identifier).assignment
            == COMM_INTERVENTION
        ):
            url = reverse("intecomm_dashboard:comm_subject_listboard_url")
        else:
            url = reverse("intecomm_dashboard:inte_subject_listboard_url")
        cnt = obj.patients.all().count()
        url = f"{url}?q={obj.group_identifier}"
        return format_html(f'<a href="{url}">{cnt}&nbsp;{p.plural("patient", cnt)}</a>')

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .exclude(status__in=[NEW, RECRUITING, COMPLETE], randomized=False)
        )
