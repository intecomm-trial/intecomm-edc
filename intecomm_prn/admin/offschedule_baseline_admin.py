from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..forms.offschedule_baseline_form import OffScheduleBaselineForm
from ..models import OffScheduleBaseline
from .offschedule_followup_admin import OffScheduleFollowupAdmin


@admin.register(OffScheduleBaseline, site=intecomm_prn_admin)
class OffScheduleBaselineAdmin(OffScheduleFollowupAdmin):

    form = OffScheduleBaselineForm
