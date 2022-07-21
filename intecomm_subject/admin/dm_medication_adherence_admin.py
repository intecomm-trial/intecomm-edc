from django.contrib import admin
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import intecomm_subject_admin

# from ..forms import DmMedicationAdherenceForm
from ..models import DmMedicationAdherence
from .modeladmin_mixins import CrfModelAdminMixin, MedicationAdherenceAdminMixin


@admin.register(DmMedicationAdherence, site=intecomm_subject_admin)
class DmMedicationAdherenceAdmin(
    MedicationAdherenceAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    pass
    # form = DmMedicationAdherenceForm
