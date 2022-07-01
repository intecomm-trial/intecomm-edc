from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin
# from ..forms import DmInitialReviewForm
from ..models import DmInitialReview
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(DmInitialReview, site=intecomm_subject_admin)
class DmInitialReviewAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):

    # form = DmInitialReviewForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diagnosis and Treatment",
            {
                "fields": (
                    "dx_ago",
                    "dx_date",
                    "managed_by",
                    "med_start_ago",
                )
            },
        ),
        (
            "Blood Sugar Measurement",
            {
                "fields": (
                    "glucose_performed",
                    "glucose_fasted",
                    "glucose_date",
                    "glucose",
                    "glucose_quantifier",
                    "glucose_units",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "managed_by": admin.VERTICAL,
        "glucose_performed": admin.VERTICAL,
        "glucose_fasted": admin.VERTICAL,
        "glucose_units": admin.VERTICAL,
    }
