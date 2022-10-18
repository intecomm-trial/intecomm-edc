from django.contrib import admin
from edc_adherence.model_admin_mixin import MedicationAdherenceAdminMixin

from ..admin_site import intecomm_subject_admin
from ..models import DmMedicationAdherence
from .modeladmin_mixins import CrfModelAdmin


@admin.register(DmMedicationAdherence, site=intecomm_subject_admin)
class DmMedicationAdherenceAdmin(MedicationAdherenceAdminMixin, CrfModelAdmin):
    pass
    # form = DmMedicationAdherenceForm
