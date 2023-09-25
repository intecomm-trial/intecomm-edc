from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import HospitalizationModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import intecomm_ae_admin
from ..forms import HospitalizationForm
from ..models import Hospitalization


@admin.register(Hospitalization, site=intecomm_ae_admin)
class HospitalizationAdmin(
    SiteModelAdminMixin, HospitalizationModelAdminMixin, SimpleHistoryAdmin
):
    form = HospitalizationForm

    # TODO: remove with Django > 4.2.5
    def get_list_filter(self, request) -> tuple[str]:
        list_filter = super().get_list_filter(request)
        self.list_filter = list_filter
        return list_filter
