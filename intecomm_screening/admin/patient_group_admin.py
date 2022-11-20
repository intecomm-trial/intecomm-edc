from decimal import Decimal

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_constants.constants import COMPLETE, NEW
from edc_utils.round_up import round_up
from intecomm_form_validators import RECRUITING

from intecomm_group.utils import verify_patient_group_ratio_raise

from ..admin_site import intecomm_screening_admin
from ..forms import PatientGroupForm
from ..models import PatientGroup
from .modeladmin_mixins import BaseModelAdminMixin


@admin.register(PatientGroup, site=intecomm_screening_admin)
class PatientGroupAdmin(BaseModelAdminMixin):

    form = PatientGroupForm

    show_object_tools = True
    change_list_template: str = "intecomm_screening/admin/patientgroup_change_list.html"

    fieldsets = (
        (
            None,
            {"fields": ("report_datetime", "name", "patients", "notes")},
        ),
        (
            "Status and rules",
            {
                "description": format_html(
                    "Please consult with your study coordinator before you "
                    "choose to override the minimum group size and/or the ratio of "
                    "NCD to HIV patients."
                ),
                "fields": ("status", "enforce_group_size_min", "enforce_ratio"),
            },
        ),
        (
            "Randomize",
            {
                "description": format_html(
                    "Complete this section when the group is COMPLETE and ready to "
                    "RANDOMIZE. <BR>Please consult with your study coordinator before "
                    "randomizing a group that does not meet the minimum group size and/or "
                    "the ratio of NCD to HIV patients. <BR>"
                    "<B>Important: THIS STEP CANNOT BE UNDONE</B"
                ),
                "fields": ("randomize_now", "confirm_randomize_now"),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "__str__",
        "opened",
        "status",
        "rounded_ratio",
        "arm",
        "members",
        "user_created",
        "created",
    )

    list_filter = (
        "status",
        "randomized",
        "report_datetime",
    )

    search_fields = (
        "name",
        "patients__name",
    )

    filter_horizontal = ("patients",)

    radio_fields = {
        "status": admin.VERTICAL,
        "randomize_now": admin.VERTICAL,
    }

    @admin.display(description="Opened", ordering="report_datetime")
    def opened(self, obj=None):
        return obj.report_datetime.date()

    @admin.display(description="Members")
    def members(self, obj=None):
        cnt = obj.patients.all().count()
        url = reverse("intecomm_screening_admin:intecomm_screening_patientlog_changelist")
        url = f"{url}?q={obj.name}"
        return format_html(f'<a href="{url}">{cnt} patients</a>')

    @admin.display(description="Arm")
    def arm(self, obj=None):
        # site_randomizers.get("intecomm") INTE or COMM
        return None

    @admin.display(description="NCD:HIV", ordering="ratio")
    def rounded_ratio(self, obj=None):
        ncd, hiv, ratio = verify_patient_group_ratio_raise(obj.patients.all())
        return f'{ncd}:{hiv} ({round_up(ratio or Decimal("0.00"), Decimal("2.00"))})'

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .filter(status__in=[NEW, RECRUITING, COMPLETE], randomized=False)
        )
