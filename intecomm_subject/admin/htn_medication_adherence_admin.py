from django.contrib import admin
from edc_adherence.model_admin_mixin import MedicationAdherenceAdminMixin

from ..admin_site import intecomm_subject_admin
from ..models import HtnMedicationAdherence
from .modeladmin_mixins import CrfModelAdmin


@admin.register(HtnMedicationAdherence, site=intecomm_subject_admin)
class HtnMedicationAdherenceAdmin(MedicationAdherenceAdminMixin, CrfModelAdmin):
    pass

    # form = HtnMedicationAdherenceForm
