from django.contrib import admin
from edc_he.modeladmin_mixins import HealthEconomicsAssetsModelAdminMixin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsAssetsForm
from ...models import HealthEconomicsAssets
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(HealthEconomicsAssets, site=intecomm_subject_admin)
class HealthEconomicsAssetsAdmin(
    HealthEconomicsAssetsModelAdminMixin,
    CrfModelAdmin,
):
    form = HealthEconomicsAssetsForm
