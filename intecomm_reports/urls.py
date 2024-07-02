from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "intecomm_reports"

urlpatterns = [
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
