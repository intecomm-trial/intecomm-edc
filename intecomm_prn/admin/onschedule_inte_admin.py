from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..models import OnScheduleInte
from .modeladmin_mixins import OnScheduleModelAdmin


@admin.register(OnScheduleInte, site=intecomm_prn_admin)
class OnScheduleInteAdmin(OnScheduleModelAdmin):
    pass
