from django.urls.conf import path, re_path
from django.views.generic import RedirectView

from .views import ToGroupView

app_name = "intecomm_screening"
urlpatterns = [
    re_path(
        r"^to_group/(?P<ct>\d+)/"
        r"(?P<group_pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/"  # noqa
        r"(?P<ids>([a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})(,\s*[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})*)/$",  # noqa
        ToGroupView.as_view(),
        name="to_group_url",
    ),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
