from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin
from ..forms import HealthEconomicsBaselineForm
from ..models import HealthEconomicsBaseline
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsBaseline, site=intecomm_subject_admin)
class HealthEconomicsBaselineAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = HealthEconomicsBaselineForm

    additional_instructions = [
        "We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community. "
    ]
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Section 1: Household head",
            {
                "fields": (
                    "hoh",
                    "relationship_to_hoh",
                    "hoh_gender",
                    "hoh_age",
                    "hoh_citizen",
                    "hoh_religion",
                    "hoh_ethnicity",
                    "hoh_education",
                    "hoh_employment",
                    "hoh_employment_type",
                    "hoh_marital_status",
                    "hoh_insurance",
                    "hh_count",
                    "hh_minors_count",
                ),
            },
        ),
        (
            "Section 1B: Household",
            {
                "description": (
                    "A person or persons (people/ members) who share the same kitchen (pot), "
                    "live together, and run the household expenditure from the same income "
                    "is known as a ‘household”. Household members should be identified on "
                    "the basis that they shared a place of living together most of time for "
                    "the past one year. When it is difficult to demarcate “most of the time”, "
                    "living together for the past six months or more should be used to find "
                    "out whether or not the person is a household member. "
                ),
                "fields": (
                    "hh_count",
                    "hh_minors_count",
                ),
            },
        ),
        (
            "Section 1C: Patient characteristics",
            {
                "fields": (
                    "pat_citizen",
                    "pat_education",
                    "pat_employment",
                    "pat_employment_type",
                    "pat_ethnicity",
                    "pat_insurance",
                    "pat_marital_status",
                    "pat_religion",
                )
            },
        ),
        (
            "Section 2A: Household assets and income",
            {
                "fields": (
                    "residence_ownership",
                    "dwelling_value_known",
                    "dwelling_value",
                    "rooms",
                    "bedrooms",
                    "beds",
                    "water_source",
                    "water_obtain_time",
                    "toilet",
                    "roof_material",
                    "eaves",
                    "external_wall_material",
                    "external_wall_material_other",
                    "external_window_material",
                    "external_window_material_other",
                    "window_screens",
                    "window_screen_type",
                    "floor_material",
                    "electricity",
                    "lighting_source",
                    "cooking_fuel",
                )
            },
        ),
        (
            "Section 2B: Household assets and income (continued)",
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
        "crf_status": admin.VERTICAL,
    }

    filter_horizontal = []
