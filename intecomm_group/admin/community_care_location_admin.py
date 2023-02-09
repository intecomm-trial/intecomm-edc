from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_prn.modeladmin_mixins import PrnModelAdminMixin

from ..admin_site import intecomm_group_admin
from ..forms import CommunityCareLocationForm
from ..models import CommunityCareLocation


@admin.register(CommunityCareLocation, site=intecomm_group_admin)
class CommunityCareLocationAdmin(
    PrnModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = CommunityCareLocationForm

    date_hierarchy = "report_datetime"

    show_object_tools = True
    change_list_template: str = "intecomm_group/admin/communitycarelocation_change_list.html"

    fieldsets = (
        [
            None,
            {"fields": ("report_datetime",)},
        ],
        [
            "Description",
            {
                "fields": (
                    "name",
                    "location_type",
                    "location_type_other",
                    "opening_date",
                    "closing_date",
                    "description",
                ),
            },
        ],
        [
            "GPS (if available)",
            {
                "description": (
                    "Using google maps, right mouse click on the map point to copy to "
                    "clipboard, Paste here as is"
                ),
                "fields": (
                    "gps",
                    "latitude",
                    "longitude",
                ),
            },
        ],
        [
            "Notes",
            {"fields": ("notes",)},
        ],
        audit_fieldset_tuple,
    )

    list_display = ("__str__", "status", "opening_date", "closing_date", "meetings", "map")

    list_filter = ("opening_date", "closing_date")

    radio_fields = {
        "location_type": admin.VERTICAL,
    }

    readonly_fields = ("latitude", "longitude")

    search_fields = ("name",)

    @admin.display(description="Map")
    def map(self, obj=None):
        if obj.latitude and obj.longitude:
            return format_html(
                f'<A href="https://www.google.com/maps/@{obj.latitude},{obj.longitude},15z">'
                '<i class="fas fa-location-dot"></i>'
            )
        return None

    @admin.display(description="Meetings")
    def meetings(self, obj=None):
        url = reverse("intecomm_group_admin:intecomm_group_patientgroupappointment_changelist")
        search_term = "+".join(obj.name.split(" "))
        name = "&nbsp;".join(obj.name.split(" "))
        return format_html(f'<a href="{url}?q={search_term}">@{name}</a>')
