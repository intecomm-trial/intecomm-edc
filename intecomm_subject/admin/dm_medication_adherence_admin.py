from django.contrib import admin

from ..admin_site import intecomm_subject_admin
from ..forms import DmMedicationAdherenceForm
from ..models import DmMedicationAdherence
from .modeladmin_mixins import CrfModelAdmin, MedicationAdherenceAdminMixin


@admin.register(DmMedicationAdherence, site=intecomm_subject_admin)
class DmMedicationAdherenceAdmin(MedicationAdherenceAdminMixin, CrfModelAdmin):
    form = DmMedicationAdherenceForm
