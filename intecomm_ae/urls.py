from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "intecomm_ae"

urlpatterns = [
    path("", RedirectView.as_view(url="/intecomm_ae/admin/"), name="home_url"),
]
