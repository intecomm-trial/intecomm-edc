from django.contrib import admin

from ..admin_site import intecomm_subject_admin
from ..forms import HtnMedicationAdherenceForm
from ..models import HtnMedicationAdherence
from .modeladmin_mixins import CrfModelAdmin, MedicationAdherenceAdminMixin


@admin.register(HtnMedicationAdherence, site=intecomm_subject_admin)
class HtnMedicationAdherenceAdmin(MedicationAdherenceAdminMixin, CrfModelAdmin):
    form = HtnMedicationAdherenceForm
