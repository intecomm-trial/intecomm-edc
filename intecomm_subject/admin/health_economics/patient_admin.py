from django.contrib import admin
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
from ...forms import HealthEconomicsPatientForm
from ...models import HealthEconomicsPatient
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsPatient, site=intecomm_subject_admin)
class HealthEconomicsPatientAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):
    form = HealthEconomicsPatientForm

    additional_instructions = [
        "We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community. "
    ]
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Patient characteristics",
            {
                "fields": (
                    "pat_citizen",
                    "pat_religion",
                    "pat_religion_other",
                    "pat_ethnicity",
                    "pat_ethnicity_other",
                    "pat_education",
                    "pat_education_other",
                    "pat_employment",
                    "pat_employment_type",
                    "pat_marital_status",
                    "pat_marital_status_other",
                    "pat_insurance",
                    "pat_insurance_other",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "pat_citizen": admin.VERTICAL,
        "pat_education": admin.VERTICAL,
        "pat_employment": admin.VERTICAL,
        "pat_employment_type": admin.VERTICAL,
        "pat_ethnicity": admin.VERTICAL,
        "pat_marital_status": admin.VERTICAL,
        "pat_religion": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }

    filter_horizontal = ["pat_insurance"]

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if getattr(request, "site", None):
            if db_field.name == "pat_religion":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_RELIGION_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_RELIGION_CHOICES
            if db_field.name == "pat_ethnicity":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_ETHNICITY_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_ETHNICITY_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)
