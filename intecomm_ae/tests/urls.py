from django.contrib import admin
from django.urls.conf import include, path

from intecomm_ae.admin_site import intecomm_ae_admin

urlpatterns = [
    path("ae/", include("intecomm_ae.urls")),
    path("admin/", intecomm_ae_admin.urls),
    path("admin/", admin.site.urls),
]
