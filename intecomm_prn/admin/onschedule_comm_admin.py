from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..models import OnScheduleComm
from .modeladmin_mixins import OnScheduleModelAdmin


@admin.register(OnScheduleComm, site=intecomm_prn_admin)
class OnScheduleCommAdmin(OnScheduleModelAdmin):
    pass
