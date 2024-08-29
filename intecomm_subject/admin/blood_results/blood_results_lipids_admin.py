from django.contrib import admin
from edc_action_item import action_fieldset_tuple
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import intecomm_subject_admin
from ...forms import BloodResultsLipidsForm
from ...models import BloodResultsLipids
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(BloodResultsLipids, site=intecomm_subject_admin)
class BloodResultsLipidsAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsLipidsForm
    fieldsets = BloodResultFieldset(
        BloodResultsLipids.lab_panel,
        model_cls=BloodResultsLipids,
        extra_fieldsets=[
            (-1, action_fieldset_tuple),
        ],
    ).fieldsets
