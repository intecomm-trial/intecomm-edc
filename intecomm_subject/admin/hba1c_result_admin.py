from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin
# from ..forms import Hba1cResultForm
from ..models import Hba1cResult
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Hba1cResult, site=intecomm_subject_admin)
class Hba1cResultAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):
    # form = Hba1cResultForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Result", {"fields": ("drawn_date", "result")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
    }
