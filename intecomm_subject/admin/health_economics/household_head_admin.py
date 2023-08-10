from django.contrib import admin
from django.db.models import Q
from edc_he.modeladmin_mixins import HealthEconomicsHouseholdHeadModelAdminMixin
from edc_he.models import Ethnicities, Religions

from ...admin_site import intecomm_subject_admin
from ...forms import HealthEconomicsHouseholdHeadForm
from ...models import HealthEconomicsHouseholdHead
from ..modeladmin_mixins import CrfModelAdmin


@admin.register(HealthEconomicsHouseholdHead, site=intecomm_subject_admin)
class HealthEconomicsHouseholdHeadAdmin(
    HealthEconomicsHouseholdHeadModelAdminMixin, CrfModelAdmin
):
    form = HealthEconomicsHouseholdHeadForm

    save_on_top = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if getattr(request, "site", None):
            if db_field.name == "hoh_ethnicity":
                kwargs["queryset"] = Ethnicities.objects.filter(
                    Q(extra_value=request.site.siteprofile.country)
                    | Q(extra_value__isnull=True)
                )
            if db_field.name == "hoh_religion":
                kwargs["queryset"] = Religions.objects.filter(
                    Q(extra_value=request.site.siteprofile.country)
                    | Q(extra_value__isnull=True)
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if getattr(request, "site", None):
            if db_field.name == "hoh_insurance":
                model_cls = getattr(self.model, db_field.name).field.related_model
                kwargs["queryset"] = model_cls.objects.filter(
                    Q(extra_value=request.site.siteprofile.country)
                    | Q(extra_value__isnull=True)
                )
        return super().formfield_for_manytomany(db_field, request, **kwargs)
