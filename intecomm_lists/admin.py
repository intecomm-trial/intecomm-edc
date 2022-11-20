from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from .admin_site import intecomm_lists_admin
from .models import Conditions, OffstudyReasons, SubjectVisitMissedReasons


@admin.register(SubjectVisitMissedReasons, site=intecomm_lists_admin)
class SubjectVisitMissedReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OffstudyReasons, site=intecomm_lists_admin)
class OffstudyReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Conditions, site=intecomm_lists_admin)
class ConditionsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass
