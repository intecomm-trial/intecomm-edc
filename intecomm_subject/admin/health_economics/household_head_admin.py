from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsHouseholdHeadForm
from ...models import HealthEconomicsHouseholdHead
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsHouseholdHead, site=intecomm_subject_admin)
class HealthEconomicsHouseholdHeadAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = HealthEconomicsHouseholdHeadForm

    additional_instructions = [
        "We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community. "
    ]
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Household head",
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
            "Household",
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
        "crf_status": admin.VERTICAL,
    }

    filter_horizontal = ["hoh_insurance"]
