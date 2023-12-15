from django.contrib import admin
from edc_sites.site import sites

from ..admin_site import intecomm_screening_admin
from ..models import Site


@admin.register(Site, site=intecomm_screening_admin)
class SiteAdmin(admin.ModelAdmin):
    search_fields = ("id", "name")

    def get_queryset(self, request):
        country = sites.get_current_country(request)
        return self.model.objects.filter(siteprofile__country=country).order_by("name")
