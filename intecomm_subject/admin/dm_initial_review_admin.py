from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_glucose.fieldsets import glucose_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import DmInitialReviewForm
from ..models import DmInitialReview
from .modeladmin_mixins import CrfModelAdmin


@admin.register(DmInitialReview, site=intecomm_subject_admin)
class DmInitialReviewAdmin(CrfModelAdmin):
    form = DmInitialReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diagnosis",
            {
                "fields": (
                    "dx_date",
                    "dx_ago",
                )
            },
        ),
        (
            "Treatment",
            {
                "fields": (
                    "managed_by",
                    "managed_by_other",
                    "rx_init_date",
                    "rx_init_ago",
                )
            },
        ),
        glucose_fieldset_tuple,
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ["managed_by"]

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "glucose_performed": admin.VERTICAL,
        "glucose_quantifier": admin.VERTICAL,
        "glucose_units": admin.VERTICAL,
        "glucose_fasting": admin.VERTICAL,
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        form = self.replace_label_text(form, "diagnosis_label", self.model.diagnosis_label)
        return form
