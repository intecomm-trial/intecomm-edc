from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple

from ..admin_site import intecomm_subject_admin
from ..models import Medications
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Medications, site=intecomm_subject_admin)
class MedicationsAdmin(CrfModelAdmin):
    # form = MedicationsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Prescriptions", {"fields": ("refill_htn", "refill_dm", "refill_hiv")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "refill_htn": admin.VERTICAL,
        "refill_dm": admin.VERTICAL,
        "refill_hiv": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
