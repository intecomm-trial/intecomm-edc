from edc_protocol import Protocol

from .patterns import screening_identifier
from .views import (  # SubjectListboardView,
    AeListboardView,
    CommSubjectListboardView,
    DeathReportListboardView,
    InteSubjectListboardView,
    ScreenGroupListboardView,
    SubjectDashboardView,
)

app_name = "intecomm_dashboard"

# urlpatterns = SubjectListboardView.urls(
#     namespace=app_name,
#     label="subject_listboard",
#     identifier_pattern=Protocol().subject_identifier_pattern,
# )
urlpatterns = InteSubjectListboardView.urls(
    namespace=app_name,
    label="inte_subject_listboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)
urlpatterns += CommSubjectListboardView.urls(
    namespace=app_name,
    label="comm_subject_listboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)
urlpatterns += ScreenGroupListboardView.urls(
    namespace=app_name,
    label="screen_group_listboard",
    identifier_label="screening_identifier",
    identifier_pattern=screening_identifier,
)
urlpatterns += SubjectDashboardView.urls(
    namespace=app_name,
    label="subject_dashboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)

urlpatterns += AeListboardView.urls(
    namespace=app_name,
    label="ae_listboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)
urlpatterns += DeathReportListboardView.urls(
    namespace=app_name,
    label="death_report_listboard",
    identifier_pattern=Protocol().subject_identifier_pattern,
)
