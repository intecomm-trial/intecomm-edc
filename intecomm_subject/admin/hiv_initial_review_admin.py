from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..forms import HivInitialReviewForm
from ..models import HivInitialReview
from .modeladmin_mixins import CrfModelAdmin


@admin.register(HivInitialReview, site=intecomm_subject_admin)
class HivInitialReviewAdmin(CrfModelAdmin):
    form = HivInitialReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diagnosis and Care",
            {
                "fields": (
                    "dx_date",
                    "dx_ago",
                    "receives_care",
                    "clinic",
                    "clinic_other",
                )
            },
        ),
        (
            "Monitoring and Treatment",
            {
                "fields": (
                    "rx_init",
                    "rx_init_date",
                    "rx_init_ago",
                    "has_vl",
                    "drawn_date",
                    "vl",
                    "vl_quantifier",
                    "has_cd4",
                    "cd4",
                    "cd4_date",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "rx_init": admin.VERTICAL,
        "clinic": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
        "has_cd4": admin.VERTICAL,
        "has_vl": admin.VERTICAL,
        "receives_care": admin.VERTICAL,
        "vl_quantifier": admin.VERTICAL,
    }

    def get_list_filter(self, request):
        list_filters = super().get_list_filter(request)
        list_filters = list(list_filters or [])
        list_filters.insert(4, "has_vl")
        return tuple(list_filters)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        form = self.replace_label_text(form, "diagnosis_label", self.model.diagnosis_label)
        return form
