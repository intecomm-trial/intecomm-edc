from django.contrib import admin
from edc_he.modeladmin_mixins import HealthEconomicsPropertyModelAdminMixin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsPropertyForm
from ...models import HealthEconomicsProperty
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(HealthEconomicsProperty, site=intecomm_subject_admin)
class HealthEconomicsPropertyAdmin(HealthEconomicsPropertyModelAdminMixin, CrfModelAdmin):
    form = HealthEconomicsPropertyForm
