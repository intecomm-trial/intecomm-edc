from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..forms import OffScheduleCommForm
from ..models import OffScheduleComm
from .offschedule_inte_admin import OffScheduleInteAdmin


@admin.register(OffScheduleComm, site=intecomm_prn_admin)
class OffScheduleCommAdmin(OffScheduleInteAdmin):
    form = OffScheduleCommForm
