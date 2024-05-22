from django.contrib import admin
from django.contrib.admin import ModelAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ...admin_site import intecomm_subject_admin
from ...models import CurrentConditions


@admin.register(CurrentConditions, site=intecomm_subject_admin)
class CurrentConditionsAdmin(ModelAdminSubjectDashboardMixin, ModelAdmin):
    list_display = (
        "subject_identifier",
        "dashboard",
        "baseline_date",
        "hiv",
        "htn",
        "dm",
        "created",
        "comment",
    )
    list_filter = ("hiv", "htn", "dm")
    readonly_fields = ("subject_identifier", "hiv", "htn", "dm")
