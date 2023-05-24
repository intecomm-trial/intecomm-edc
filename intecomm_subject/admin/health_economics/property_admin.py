from django.contrib import admin
from edc_form_label import FormLabelModelAdminMixin
from edc_he.modeladmin_mixins import HealthEconomicsPropertyModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsPropertyForm
from ...models import HealthEconomicsProperty
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsProperty, site=intecomm_subject_admin)
class HealthEconomicsPropertyAdmin(
    HealthEconomicsPropertyModelAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = HealthEconomicsPropertyForm
