from django.contrib import admin

from ..admin_site import intecomm_group_admin
from ..models import PatientLog


@admin.register(PatientLog, site=intecomm_group_admin)
class PatientLogAdmin(admin.ModelAdmin):
    """Registered again for the autocomplete field"""

    search_fields = ("name",)
