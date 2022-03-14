from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from .admin_site import intecomm_lists_admin
from .models import OffstudyReasons, SubjectVisitMissedReasons


@admin.register(SubjectVisitMissedReasons, site=intecomm_lists_admin)
class SubjectVisitMissedReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OffstudyReasons, site=intecomm_lists_admin)
class OffstudyReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass
