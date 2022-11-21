from django.contrib import admin

from ..admin_site import intecomm_screening_admin
from ..models import Site


@admin.register(Site, site=intecomm_screening_admin)
class SiteAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "name",
    )
