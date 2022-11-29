from django.contrib import admin
from django.utils.html import format_html
from edc_sites import get_site_name

from intecomm_sites import all_sites

from ..admin_site import intecomm_screening_admin
from ..forms import HealthFacilityForm
from ..models import HealthFacility
from .modeladmin_mixins import BaseModelAdminMixin


@admin.register(HealthFacility, site=intecomm_screening_admin)
class HealthFacilityAdmin(BaseModelAdminMixin):
    form = HealthFacilityForm
    show_object_tools = True
    change_list_template: str = "intecomm_screening/admin/healthfacility_change_list.html"
    change_list_title = HealthFacility._meta.verbose_name_plural
    change_list_note = "These are health facilites within a hospital"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "name",
                    "health_facility_type",
                    "health_facility_type_other",
                )
            },
        ),
        (
            "Location",
            {
                "description": "Provide this information if available",
                "fields": (
                    "distance",
                    "gps",
                    "latitude",
                    "longitude",
                ),
            },
        ),
        (
            "Notes",
            {
                "fields": ("notes",),
            },
        ),
    )

    list_display = (
        "name",
        "health_facility_type",
        "distance",
        "map",
    )

    list_filter = (
        "report_datetime",
        "health_facility_type",
    )

    radio_fields = {
        "health_facility_type": admin.VERTICAL,
    }

    search_fields = (
        "name",
        "health_facility_type__name",
    )

    @admin.display(description="Map")
    def map(self, obj=None):
        if obj.latitude and obj.longitude:
            return format_html(
                f'<A href="https://www.google.com/maps/@{obj.latitude},{obj.longitude},15z">'
                '<i class="fas fa-location-dot"></i>'
            )
        return None

    @staticmethod
    def site_name(obj=None):
        get_site_name(obj.site.id, all_sites)
        return obj.name
