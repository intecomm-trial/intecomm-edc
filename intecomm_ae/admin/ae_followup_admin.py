from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeFollowupModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_ae_admin
from ..forms import AeFollowupForm
from ..models import AeFollowup


@admin.register(AeFollowup, site=intecomm_ae_admin)
class AeFollowupAdmin(SiteModelAdminMixin, AeFollowupModelAdminMixin, SimpleHistoryAdmin):
    form = AeFollowupForm

    # TODO: remove with Django > 4.2.5
    def get_list_filter(self, request) -> tuple[str]:
        list_filter = super().get_list_filter(request)
        self.list_filter = list_filter
        return list_filter
