from django.contrib import admin
from edc_adherence.model_admin_mixin import MedicationAdherenceAdminMixin

from ..admin_site import intecomm_subject_admin
from ..forms import HivMedicationAdherenceForm
from ..models import HivMedicationAdherence
from .modeladmin_mixins import CrfModelAdmin


@admin.register(HivMedicationAdherence, site=intecomm_subject_admin)
class HivMedicationAdherenceAdmin(MedicationAdherenceAdminMixin, CrfModelAdmin):
    form = HivMedicationAdherenceForm
