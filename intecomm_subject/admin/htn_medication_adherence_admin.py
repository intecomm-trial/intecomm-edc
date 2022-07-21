from django.contrib import admin
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin

# from ..forms import HtnMedicationAdherenceForm
from ..models import HtnMedicationAdherence
from .modeladmin_mixins import CrfModelAdminMixin, MedicationAdherenceAdminMixin


@admin.register(HtnMedicationAdherence, site=intecomm_subject_admin)
class HtnMedicationAdherenceAdmin(
    MedicationAdherenceAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    pass

    # form = HtnMedicationAdherenceForm
