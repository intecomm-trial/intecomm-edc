from django.contrib import admin
from edc_form_label import FormLabelModelAdminMixin
from edc_he.modeladmin_mixins import HealthEconomicsIncomeModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsIncomeForm
from ...models import HealthEconomicsIncome
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsIncome, site=intecomm_subject_admin)
class HealthEconomicsIncomeAdmin(
    HealthEconomicsIncomeModelAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = HealthEconomicsIncomeForm
