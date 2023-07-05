from django.contrib import admin
from edc_he.modeladmin_mixins import HealthEconomicsIncomeModelAdminMixin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsIncomeForm
from ...models import HealthEconomicsIncome
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(HealthEconomicsIncome, site=intecomm_subject_admin)
class HealthEconomicsIncomeAdmin(HealthEconomicsIncomeModelAdminMixin, CrfModelAdmin):
    form = HealthEconomicsIncomeForm
