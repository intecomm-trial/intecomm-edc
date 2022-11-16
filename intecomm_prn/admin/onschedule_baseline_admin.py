from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..models import OnScheduleBaseline
from .onschedule_followup_admin import OnScheduleFollowupAdmin


@admin.register(OnScheduleBaseline, site=intecomm_prn_admin)
class OnScheduleBaselineAdmin(OnScheduleFollowupAdmin):

    pass
