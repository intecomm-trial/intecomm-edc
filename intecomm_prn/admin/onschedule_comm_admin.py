from __future__ import annotations

from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..models import OnScheduleComm
from .modeladmin_mixins import OnScheduleModelAdmin


@admin.register(OnScheduleComm, site=intecomm_prn_admin)
class OnScheduleCommAdmin(OnScheduleModelAdmin):
    # TODO: remove with Django > 4.2.5
    def get_list_filter(self, request) -> tuple[str]:
        list_filter = super().get_list_filter(request)
        self.list_filter = list_filter
        return list_filter
