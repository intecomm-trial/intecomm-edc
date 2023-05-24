from django.contrib import admin
from edc_form_label import FormLabelModelAdminMixin
from edc_he.modeladmin_mixins import HealthEconomicsPatientModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ...admin_site import intecomm_subject_admin
from ...choices import (
    TZ_ETHNICITY_CHOICES,
    TZ_RELIGION_CHOICES,
    UG_ETHNICITY_CHOICES,
    UG_RELIGION_CHOICES,
)
from ...forms import HealthEconomicsPatientForm
from ...models import HealthEconomicsPatient
from ..modeladmin_mixins import CrfModelAdminMixin


@admin.register(HealthEconomicsPatient, site=intecomm_subject_admin)
class HealthEconomicsPatientAdmin(
    HealthEconomicsPatientModelAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = HealthEconomicsPatientForm

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if getattr(request, "site", None):
            if db_field.name == "pat_religion":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_RELIGION_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_RELIGION_CHOICES
            if db_field.name == "pat_ethnicity":
                if request.site.siteprofile.country == "uganda":
                    kwargs["choices"] = UG_ETHNICITY_CHOICES
                elif request.site.siteprofile.country == "tanzania":
                    kwargs["choices"] = TZ_ETHNICITY_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)
