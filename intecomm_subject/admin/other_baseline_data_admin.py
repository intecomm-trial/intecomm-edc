from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import OtherBaselineData
from .modeladmin_mixins import CrfModelAdmin


@admin.register(OtherBaselineData, site=intecomm_subject_admin)
class OtherBaselineDataAdmin(CrfModelAdmin):
    # form = OtherBaselineDataForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Smoking", {"fields": ("smoking_status", "smoker_quit_ago")}),
        ("Alcohol", {"fields": ("alcohol", "alcohol_consumption")}),
        ("Diet", {"fields": ("num_vegetables_eaten", "use_salt_on_food")}),
        (
            "Physical activity",
            {
                "fields": (
                    "work_activity",
                    "work_activity_days",
                    "work_activity_exercise",
                    "work_activity_exercise_time",
                )
            },
        ),
        (
            "Other",
            {
                "fields": (
                    "employment_status",
                    "employment_status_other",
                    "education",
                    "marital_status",
                )
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "smoking_status": admin.VERTICAL,
        "alcohol": admin.VERTICAL,
        "alcohol_consumption": admin.VERTICAL,
        "employment_status": admin.VERTICAL,
        "education": admin.VERTICAL,
        "marital_status": admin.VERTICAL,
        "work_activity": admin.VERTICAL,
        "use_salt_on_food": admin.VERTICAL,
    }
