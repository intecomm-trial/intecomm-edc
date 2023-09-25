from __future__ import annotations

from django.contrib import admin
from edc_action_item import ActionItemModelAdminMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin
from edc_transfer.modeladmin_mixins import SubjectTransferModelAdminMixin

from ..admin_site import intecomm_prn_admin
from ..forms import SubjectTransferForm
from ..models import SubjectTransfer


@admin.register(SubjectTransfer, site=intecomm_prn_admin)
class SubjectTransferAdmin(
    SiteModelAdminMixin,
    SubjectTransferModelAdminMixin,
    ActionItemModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectTransferForm

    # TODO: remove with Django > 4.2.5
    def get_list_filter(self, request) -> tuple[str]:
        list_filter = super().get_list_filter(request)
        self.list_filter = list_filter
        return list_filter
