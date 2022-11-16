from django.contrib import admin

from intecomm_prn.models import PatientLog

from ..admin_site import intecomm_prn_admin


@admin.register(PatientLog, site=intecomm_prn_admin)
class PatientLogAdmin(admin.ModelAdmin):
    """Registered again for the autocomplete field"""

    search_fields = ("name",)
