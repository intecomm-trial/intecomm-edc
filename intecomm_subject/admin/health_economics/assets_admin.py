from django.contrib import admin
from edc_constants.constants import OPTION_RETIRED
from edc_he.choices import EXTERNAL_WALL_MATERIALS_CHOICES
from edc_he.modeladmin_mixins import HealthEconomicsAssetsModelAdminMixin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsAssetsForm
from ...models import HealthEconomicsAssets
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(HealthEconomicsAssets, site=intecomm_subject_admin)
class HealthEconomicsAssetsAdmin(
    HealthEconomicsAssetsModelAdminMixin,
    CrfModelAdmin,
):
    form = HealthEconomicsAssetsForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        if getattr(request, "site", None):
            if request.site.siteprofile.country == "uganda":
                index = 0
                fieldsets = list(fieldsets)
                for label, data in fieldsets:
                    if label == "Household assets (continued)":
                        data["fields"] = tuple([f for f in data["fields"] if f != "dala_dala"])
                        fieldsets[index] = (label, data)
                    index += 1
                fieldsets = tuple(fieldsets)
        return fieldsets

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "external_wall_material":
            kwargs["choices"] = self.external_wall_material_choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    @property
    def external_wall_material_choices(self) -> tuple[tuple[str, str]]:
        choices: list[tuple[str, str]] = []
        for tpl in EXTERNAL_WALL_MATERIALS_CHOICES:
            if tpl[0] != OPTION_RETIRED:
                choices.append(tpl)
        return tuple(choices)
