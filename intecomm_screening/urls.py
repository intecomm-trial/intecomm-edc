from django.urls.conf import path, re_path
from django.views.generic import RedirectView

from .views import GroupManagementView

app_name = "intecomm_screening"
urlpatterns = [
    re_path(
        r"^group_managment/(?P<ct>\d+)/"
        r"(?P<ids>([a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})(,\s*[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})*)/$",  # noqa
        GroupManagementView.as_view(),
        name="group_managment_url",
    ),
    # re_path(
    #     r"^print_patient_log_report/(?P<id>\d+)/$",
    #     PrintPatientLogReportView.as_view(),
    #     name="print_patient_log_report_url",
    # ),
    path("", RedirectView.as_view(url=f"/{app_name}/admin/"), name="home_url"),
]
