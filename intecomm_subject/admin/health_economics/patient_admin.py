from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
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
