from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "intecomm_export"

urlpatterns = [
    path("", RedirectView.as_view(url="/intecomm_export/admin/"), name="home_url"),
]
