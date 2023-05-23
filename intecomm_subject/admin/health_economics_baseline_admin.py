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
        (
            "Section 2C: Household assets and income (continued)",
            {
                "description": format_html(
                    "I would now like to know if you own any <B>land or other property</B> "
                    "– and the approximate value (amount). I know this is sensitive "
                    "information and will not share this with any persons outside of the "
                    "survey team. <B><U>There is no need to give details or show me any of "
                    "the items.</U></B>"
                ),
                "fields": (
                    "land_owner",
                    "land_value_known",
                    "land_value",
                    "land_additional",
                    "land_additional_known",
                    "land_additional_value",
                ),
            },
        ),
        (
            "Section 2D: Household assets and income (continued)",
            {
                "description": format_html(
                    "Now, I will ask about income for the household from paid work or "
                    "other sources. I know it may be difficult to calculate those figures, "
                    "but please do try to give amounts as accurately as possible. Remember "
                    "that all information will be kept strictly confidential. This "
                    "information is important to assess overall health and well-being of "
                    "people in your household, compared to other similar households.<BR><BR>"
                    "I am now going to read you a list of possible sources of income. "
                    "Thinking over the last 12 months, can you tell me what the average "
                    "earnings of the household have been per week or per month or per year? "
                    "Please tell me whichever time period that is easier for you."
                ),
                "fields": (
                    "wages",
                    "wages_value_known",
                    "wages_value",
                    "selling",
                    "selling_value_known",
                    "selling_value",
                    "rental_income",
                    "rental_income_value_known",
                    "rental_income_value",
                    "pension",
                    "pension_value_known",
                    "pension_value",
                    "ngo_assistance",
                    "ngo_assistance_value_known",
                    "ngo_assistance_value",
                    "interest",
                    "interest_value_known",
                    "interest_value",
                    "internal_remittance",
                    "internal_remittance_value_known",
                    "internal_remittance_value",
                    "external_remittance",
                    "external_remittance_value_known",
                    "external_remittance_value",
                    "external_remittance_currency",
                    "external_remittance_currency_other",
                    "more_sources",
                    "more_sources_other",
                    "more_sources_value_known",
                    "more_sources_value",
                    "external_dependents",
                    "income_enough",
                    "financial_status",
                    "financial_status_compare",
                    "household_debt",
                    "household_debt_value",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "hoh": admin.VERTICAL,
        "relationship_to_hoh": admin.VERTICAL,
        "hoh_gender": admin.VERTICAL,
        "hoh_citizen": admin.VERTICAL,
        "hoh_religion": admin.VERTICAL,
        "hoh_ethnicity": admin.VERTICAL,
        "hoh_education": admin.VERTICAL,
        "hoh_employment": admin.VERTICAL,
        "hoh_employment_type": admin.VERTICAL,
        "hoh_marital_status": admin.VERTICAL,
        "pat_citizen": admin.VERTICAL,
        "pat_education": admin.VERTICAL,
        "pat_employment": admin.VERTICAL,
        "pat_employment_type": admin.VERTICAL,
        "pat_ethnicity": admin.VERTICAL,
        "pat_marital_status": admin.VERTICAL,
        "pat_religion": admin.VERTICAL,
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
        "land_owner": admin.VERTICAL,
        "land_value_known": admin.VERTICAL,
        "land_additional": admin.VERTICAL,
        "land_additional_known": admin.VERTICAL,
        "wages": admin.VERTICAL,
        "wages_value_known": admin.VERTICAL,
        "selling": admin.VERTICAL,
        "selling_value_known": admin.VERTICAL,
        "rental_income": admin.VERTICAL,
        "rental_income_value_known": admin.VERTICAL,
        "pension": admin.VERTICAL,
        "pension_value_known": admin.VERTICAL,
        "ngo_assistance": admin.VERTICAL,
        "ngo_assistance_value_known": admin.VERTICAL,
        "interest": admin.VERTICAL,
        "interest_value_known": admin.VERTICAL,
        "internal_remittance": admin.VERTICAL,
        "internal_remittance_value_known": admin.VERTICAL,
        "external_remittance": admin.VERTICAL,
        "external_remittance_value_known": admin.VERTICAL,
        # "external_remittance_currency": admin.VERTICAL,
        "more_sources": admin.VERTICAL,
        "more_sources_value_known": admin.VERTICAL,
        # "external_dependents": admin.VERTICAL,
        "income_enough": admin.VERTICAL,
        "financial_status": admin.VERTICAL,
        "financial_status_compare": admin.VERTICAL,
        "household_debt": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }

    filter_horizontal = ["hoh_insurance", "pat_insurance"]
