from django.contrib import admin
from edc_form_label import FormLabelModelAdminMixin
from edc_he.modeladmin_mixins import HealthEconomicsAssetsModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsAssetsForm
from ...models import HealthEconomicsAssets
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsAssets, site=intecomm_subject_admin)
class HealthEconomicsAssetsAdmin(
    HealthEconomicsAssetsModelAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = HealthEconomicsAssetsForm
