from __future__ import annotations

from django.contrib import admin

from ..admin_site import intecomm_prn_admin
from ..forms import OffScheduleInteForm
from ..models import OffScheduleInte
from .modeladmin_mixins import OffScheduleAdmin


@admin.register(OffScheduleInte, site=intecomm_prn_admin)
class OffScheduleInteAdmin(OffScheduleAdmin):
    form = OffScheduleInteForm

    # TODO: remove with Django > 4.2.5
    def get_list_filter(self, request) -> tuple[str]:
        list_filter = super().get_list_filter(request)
        self.list_filter = list_filter
        return list_filter
