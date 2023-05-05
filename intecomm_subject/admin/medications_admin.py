from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_dx import get_diagnosis_labels_prefixes

from ..admin_site import intecomm_subject_admin
from ..forms import MedicationsForm
from ..models import Medications
from .modeladmin_mixins import CrfModelAdmin


@admin.register(Medications, site=intecomm_subject_admin)
class MedicationsAdmin(CrfModelAdmin):
    form = MedicationsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Prescriptions",
            {
                "fields": tuple(f"refill_{dx}" for dx in get_diagnosis_labels_prefixes()),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        **{f"refill_{dx}": admin.VERTICAL for dx in get_diagnosis_labels_prefixes()},
    }
