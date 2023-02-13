from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..models import OnScheduleComm
from .onschedule_inte_admin import OnScheduleInteAdmin


@admin.register(OnScheduleComm, site=intecomm_prn_admin)
class OnScheduleCommAdmin(OnScheduleInteAdmin):
    pass
