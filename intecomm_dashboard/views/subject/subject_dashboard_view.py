from __future__ import annotations

from typing import Any, Type

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from edc_sites.site import sites
from edc_subject_dashboard.views import SubjectDashboardView as BaseSubjectDashboardView
from intecomm_rando.constants import UGANDA

from intecomm_group.models import PatientGroup
from intecomm_group.utils import get_group_subject_dashboards_url
from intecomm_screening.models import PatientLog, PatientLogUg


class SubjectDashboardView(BaseSubjectDashboardView):
    navbar_selected_item = "subjects"
    visit_model = "intecomm_subject.subjectvisit"
    history_button_label = _("Audit")

    def __init__(self, **kwargs):
        self._patient_group = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        if not self.patient_group:
            group_identifier = None
            group_name = None
            patient_group_url = None
        else:
            group_identifier = self.patient_group.group_identifier
            group_name = self.patient_group.name
            patient_group_url = reverse(
                "intecomm_group_admin:intecomm_group_patientgroup_changelist"
            )
            patient_group_url = f"{patient_group_url}?q={self.patient_group.name}"
        kwargs.update(
            subject_listboard_url="screen_group_url",
            group_identifier=group_identifier,
            group_name=group_name,
            patient_group_url=patient_group_url,
            patient_log=self.patient_log,
            patient_log_url=self.patient_log_url,
            group_subject_dashboards_url=get_group_subject_dashboards_url(self.patient_log),
        )
        return super().get_context_data(**kwargs)

    @property
    def patient_log_model_cls(self) -> Type[PatientLog | PatientLogUg]:
        if sites.get_current_country(self.request) == UGANDA:
            return PatientLogUg
        return PatientLog

    @property
    def patient_group(self) -> PatientGroup | None:
        if not self._patient_group:
            if self.patient_log.group_identifier:
                self._patient_group = PatientGroup.objects.get(
                    group_identifier=self.patient_log.group_identifier
                )
        return self._patient_group

    @property
    def patient_log(self):
        if self.subject_identifier:
            return self.patient_log_model_cls.objects.get(
                subject_identifier=self.subject_identifier
            )
        return None

    @property
    def patient_log_url(self) -> str:
        if self.patient_log:
            if self.patient_log.site.siteprofile.country == UGANDA:
                patient_log_url = reverse(
                    "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
                )
            else:
                patient_log_url = reverse(
                    "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
                )
            url = f"{patient_log_url}?q={self.filing_identifier}"
        else:
            url = None
        return url

    @property
    def filing_identifier(self) -> str | None:
        if self.patient_log:
            return self.patient_log.filing_identifier
        return None
