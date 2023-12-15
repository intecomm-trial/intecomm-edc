from django.contrib import admin
from edc_facility.admin_site import edc_facility_admin
from edc_facility.modeladmin_mixins import HealthFacilityModelAdminMixin
from edc_facility.models import HealthFacility as DefaultHealthFacility
from edc_sites.admin import SiteModelAdminMixin
from edc_sites.site import sites

from intecomm_screening.admin.modeladmin_mixins import (
    BaseModelAdminMixin,
    ChangeListTopBarModelAdminMixin,
)

from .admin_site import intecomm_facility_admin
from .forms import HealthFacilityForm
from .models import HealthFacility

edc_facility_admin.unregister(DefaultHealthFacility)


@admin.register(HealthFacility, site=intecomm_facility_admin)
class HealthFacilityAdmin(
    HealthFacilityModelAdminMixin,
    SiteModelAdminMixin,
    ChangeListTopBarModelAdminMixin,
    BaseModelAdminMixin,
):
    form = HealthFacilityForm
    show_object_tools = True
    change_list_template: str = "intecomm_facility/admin/healthfacility_changelist.html"
    change_list_title = HealthFacility._meta.verbose_name_plural
    change_list_note = "These are health facilites within a hospital"

    changelist_top_bar_selected = "healthfacility"
    changelist_top_bar_add_url = "intecomm_facility_admin:intecomm_facility_healthfacility_add"

    @admin.display(description="Distance (km)", ordering="distance")
    def distance_abbrev(self, obj=None):
        return obj.distance

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        for fieldset in fieldsets:
            if fieldset[0] == "Location":
                fields = fieldset[1]["fields"]
                fields = list(fields)
                fields.insert(0, "distance")
                fieldset[1]["fields"] = tuple(fields)
                break
        return fieldsets

    def get_list_display(self, request) -> tuple[str, ...]:
        list_display = super().get_list_display(request)
        list_display = list(list_display)
        list_display.insert(4, "distance_abbrev")
        return tuple(list_display)

    def site_name(self, obj=None):
        return sites.get(obj.site.id).name
