from __future__ import annotations

from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..forms import OffScheduleCommForm
from ..models import OffScheduleComm
from .modeladmin_mixins import OffScheduleAdmin


@admin.register(OffScheduleComm, site=intecomm_prn_admin)
class OffScheduleCommAdmin(OffScheduleAdmin):
    form = OffScheduleCommForm

    # TODO: remove with Django > 4.2.5
    def get_list_filter(self, request) -> tuple[str]:
        list_filter = super().get_list_filter(request)
        self.list_filter = list_filter
        return list_filter
