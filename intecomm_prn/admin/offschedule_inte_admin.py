from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..forms import OffScheduleInteForm
from ..models import OffScheduleInte
from .modeladmin_mixins import OffScheduleAdmin


@admin.register(OffScheduleInte, site=intecomm_prn_admin)
class OffScheduleInteAdmin(OffScheduleAdmin):
    form = OffScheduleInteForm
