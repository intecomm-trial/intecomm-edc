from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin
# from ..forms import Cd4ResultForm
from ..models import Cd4Result
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Cd4Result, site=intecomm_subject_admin)
class Cd4ResultAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):
    # form = Cd4ResultForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Result", {"fields": ("drawn_date", "result")}),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
    }
