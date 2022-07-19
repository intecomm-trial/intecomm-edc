from django.contrib import admin
from django.urls.conf import include, path

from intecomm_prn.admin_site import intecomm_prn_admin

urlpatterns = [
    path("intecomm_prn/", include("intecomm_prn.urls")),
    path("admin/", intecomm_prn_admin.urls),
    path("admin/", admin.site.urls),
]
