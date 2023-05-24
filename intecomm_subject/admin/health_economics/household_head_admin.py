from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...choices import (
    TZ_ETHNICITY_CHOICES,
    TZ_RELIGION_CHOICES,
    UG_ETHNICITY_CHOICES,
    UG_RELIGION_CHOICES,
)
from ...forms import HealthEconomicsHouseholdHeadForm
from ...models import HealthEconomicsHouseholdHead
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsHouseholdHead, site=intecomm_subject_admin)
class HealthEconomicsHouseholdHeadAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = HealthEconomicsHouseholdHeadForm

    additional_instructions = format_html(
        "<H5><B><font color='orange'>Interviewer to read</font></B></H5>"
        "<p>We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community.</p>"
    )

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Household head",
            {
                "description": format_html(
                    "<H5><B><font color='orange'>Interviewer to read</font></B></H5>"
                    "<p>By <B>HEAD OF THE HOUSEHOLD</B> we mean the main decision maker "
                    "in the HOUSEHOLD. The HEAD can be either male or female. If two "
                    "people are equal decision-makers, take the older person</p>"
                ),
                "fields": (
                    "hoh",
                    "relationship_to_hoh",
                    "relationship_to_hoh_other",
                    "hoh_gender",
                    "hoh_age",
                    "hoh_citizen",
                    "hoh_religion",
                    "hoh_religion_other",
                    "hoh_ethnicity",
                    "hoh_ethnicity_other",
                    "hoh_education",
                    "hoh_education_other",
                    "hoh_employment",
                    "hoh_employment_type",
                    "hoh_marital_status",
                    "hoh_marital_status_other",
                    "hoh_insurance",
                    "hoh_insurance_other",
                ),
            },
        ),
        (
            "Household",
            {
                "description": format_html(
                    "<H5><B><font color='orange'>Interviewer to read</font></B></H5>"
                    "<p><B>HOUSEHOLD</B>: A person or persons (people/ members) who share "
                    "the same kitchen (pot), live together, and run the household "
                    "expenditure from the same income is known as a household.</P>"
                    "<P><B>HOUSEHOLD MEMBER</B>: A household member should be identified on "
                    "the basis that they shared a place of living together most of time for "
                    "the past one year.</P><P><B>Note:</B> When it is difficult to demarcate "
                    "'most of the time', living together for the past six months or more "
                    "should be used to find out whether or not the person is a "
                    "household member.</p>"
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

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if getattr(request, "site", None):
            if db_field.name == "hoh_religion":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_RELIGION_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_RELIGION_CHOICES
            if db_field.name == "hoh_ethnicity":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_ETHNICITY_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_ETHNICITY_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)
