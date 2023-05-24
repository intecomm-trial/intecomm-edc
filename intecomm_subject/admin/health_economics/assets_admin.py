from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsAssetsForm
from ...models import HealthEconomicsAssets
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsAssets, site=intecomm_subject_admin)
class HealthEconomicsAssetsAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = HealthEconomicsAssetsForm

    additional_instructions = [
        "We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community. "
    ]
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Household assets",
            {
                "fields": (
                    "residence_ownership",
                    "dwelling_value_known",
                    "dwelling_value",
                    "rooms",
                    "bedrooms",
                    "beds",
                    "water_source",
                    "water_source_other",
                    "water_obtain_time",
                    "toilet",
                    "toilet_other",
                    "roof_material",
                    "roof_material_other",
                    "eaves",
                    "external_wall_material",
                    "external_wall_material_other",
                    "external_window_material",
                    "external_window_material_other",
                    "window_screens",
                    "window_screen_type",
                    "floor_material",
                    "floor_material_other",
                    "electricity",
                    "lighting_source",
                    "lighting_source_other",
                    "cooking_fuel",
                    "cooking_fuel_other",
                )
            },
        ),
        (
            "Household assets (continued)",
            {
                "description": format_html(
                    "Does your household or anyone in your household have the following "
                    "in working order? <BR>Note: If a household owns one of the assets below "
                    "but the asset is not in working order then it should be marked as 'No'"
                ),
                "fields": (
                    "radio",
                    "television",
                    "mobile_phone",
                    "computer",
                    "telephone",
                    "fridge",
                    "generator",
                    "iron",
                    "bicycle",
                    "motorcycle",
                    "dala_dala",
                    "car",
                    "motorboat",
                    "large_livestock",
                    "small_animals",
                    "shop",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "residence_ownership": admin.VERTICAL,
        "dwelling_value_known": admin.VERTICAL,
        "water_source": admin.VERTICAL,
        "water_obtain_time": admin.VERTICAL,
        "toilet": admin.VERTICAL,
        "roof_material": admin.VERTICAL,
        "eaves": admin.VERTICAL,
        "external_wall_material": admin.VERTICAL,
        "external_window_material": admin.VERTICAL,
        "window_screens": admin.VERTICAL,
        "window_screen_type": admin.VERTICAL,
        "floor_material": admin.VERTICAL,
        "electricity": admin.VERTICAL,
        "lighting_source": admin.VERTICAL,
        "cooking_fuel": admin.VERTICAL,
        "radio": admin.VERTICAL,
        "television": admin.VERTICAL,
        "mobile_phone": admin.VERTICAL,
        "computer": admin.VERTICAL,
        "telephone": admin.VERTICAL,
        "fridge": admin.VERTICAL,
        "generator": admin.VERTICAL,
        "iron": admin.VERTICAL,
        "bicycle": admin.VERTICAL,
        "motorcycle": admin.VERTICAL,
        "dala_dala": admin.VERTICAL,
        "car": admin.VERTICAL,
        "motorboat": admin.VERTICAL,
        "large_livestock": admin.VERTICAL,
        "small_animals": admin.VERTICAL,
        "shop": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
