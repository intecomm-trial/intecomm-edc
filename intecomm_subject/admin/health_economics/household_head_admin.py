from django.contrib import admin
from edc_form_label import FormLabelModelAdminMixin
from edc_he.modeladmin_mixins import HealthEconomicsHouseholdHeadModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...choices import (
    TZ_ETHNICITY_CHOICES,
    TZ_RELIGION_CHOICES,
    UG_ETHNICITY_CHOICES,
    UG_RELIGION_CHOICES,
)
from ...forms import HealthEconomicsHouseholdHeadForm
from ...models import HealthEconomicsHouseholdHead
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsHouseholdHead, site=intecomm_subject_admin)
class HealthEconomicsHouseholdHeadAdmin(
    HealthEconomicsHouseholdHeadModelAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = HealthEconomicsHouseholdHeadForm

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if getattr(request, "site", None):
            if db_field.name == "hoh_religion":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_RELIGION_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_RELIGION_CHOICES
            if db_field.name == "hoh_ethnicity":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_ETHNICITY_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_ETHNICITY_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)
