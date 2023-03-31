from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import OtherBaselineDataForm
from ..models import OtherBaselineData
from .modeladmin_mixins import CrfModelAdmin


@admin.register(OtherBaselineData, site=intecomm_subject_admin)
class OtherBaselineDataAdmin(CrfModelAdmin):
    form = OtherBaselineDataForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Smoking",
            {"fields": ("smoking_status", "smoker_quit_ago", "smoker_current_duration")},
        ),
        ("Alcohol", {"fields": ("alcohol", "alcohol_consumption")}),
        (
            "Diet",
            {
                "fields": (
                    "num_leafy_vegs_eaten",
                    "num_other_vegs_eaten",
                    "num_fruits_eaten",
                    "adds_salt_to_food",
                )
            },
        ),
        (
            "Physical activity: Work",
            {
                "description": (
                    "<h5>INTERVIEWER NOTES</h5>"
                    "<p>We are asking about moderate or vigorous-intensity activity at "
                    "work.</p><p>By this we mean work that causes small to large increases "
                    "in breathing or heart rate for at <b>least 10 minutes</b> continuously"
                    "</p><p>Some examples might be work that involves carrying or lifting "
                    "loads, digging or construction.</p>"
                ),
                "fields": (
                    "activity_work",
                    "activity_work_days_per_wk",
                ),
            },
        ),
        (
            "Physical activity: Personal",
            {"fields": ("activity_exercise_days_per_wk",)},
        ),
        (
            "Physical activity: Average per day",
            {"fields": ("activity_combined_mn_avg_day",)},
        ),
        (
            "Employment",
            {
                "fields": (
                    "employment_status",
                    "employment_status_other",
                )
            },
        ),
        (
            "Education",
            {"fields": ("education",)},
        ),
        (
            "Marital Status",
            {"fields": ("marital_status",)},
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
        "activity_work": admin.VERTICAL,
        "adds_salt_to_food": admin.VERTICAL,
    }
