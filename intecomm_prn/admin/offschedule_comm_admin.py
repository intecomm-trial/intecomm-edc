from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..forms import OffScheduleCommForm
from ..models import OffScheduleComm
from .modeladmin_mixins import OffScheduleAdmin


@admin.register(OffScheduleComm, site=intecomm_prn_admin)
class OffScheduleCommAdmin(OffScheduleAdmin):
    form = OffScheduleCommForm
