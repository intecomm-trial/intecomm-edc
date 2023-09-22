from __future__ import annotations

from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from edc_sites import get_current_country
from edc_subject_dashboard.views import SubjectDashboardView

from intecomm_consent.models import SubjectConsentUg
from intecomm_group.models import PatientGroup
from intecomm_group.utils import get_group_subject_dashboards_url
from intecomm_screening.constants import UGANDA
from intecomm_screening.models import PatientLog, PatientLogUg

from ....model_wrappers import (
    AppointmentModelWrapper,
    SubjectConsentModelWrapper,
    SubjectConsentUgModelWrapper,
)


class DashboardView(SubjectDashboardView):
    consent_model = "intecomm_consent.subjectconsent"
    navbar_selected_item = "consented_subject"
    visit_model = "intecomm_subject.subjectvisit"
    history_button_label = _("Audit")

    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model_wrapper_cls = SubjectConsentModelWrapper

    @property
    def patient_log_model_cls(self) -> Type[PatientLog | PatientLogUg]:
        if get_current_country(request=self.request) == UGANDA:
            return PatientLogUg
        return PatientLog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            group = PatientGroup.objects.get(
                group_identifier=context.get("consent").object.group_identifier
            )
        except ObjectDoesNotExist:
            patient_group_url = None
            group_identifier = None
            group_name = None
        else:
            group_identifier = group.group_identifier
            group_name = group.name
            patient_group_url = reverse(
                "intecomm_group_admin:intecomm_group_patientgroup_changelist"
            )
            patient_group_url = f"{patient_group_url}?q={group.name}"
        context.update(
            subject_listboard_url="screen_group_url",
            group_identifier=group_identifier,
            group_name=group_name,
            patient_group_url=patient_group_url,
            patient_log=self.patient_log,
            patient_log_url=self.patient_log_url,
            group_subject_dashboards_url=get_group_subject_dashboards_url(self.patient_log),
        )
        # replace subject_consent_model_wrapper if UG
        if get_current_country(request=self.request) == UGANDA:
            subject_consent = SubjectConsentUg.objects.get(id=context["consent"].object.id)
            subject_consent_model_wrapper = SubjectConsentUgModelWrapper(subject_consent)
            context.update(
                consent=subject_consent_model_wrapper, consents=[subject_consent_model_wrapper]
            )
        return context

    @property
    def patient_log(self):
        try:
            return self.patient_log_model_cls.objects.get(
                subject_identifier=self.subject_identifier
            )
        except ObjectDoesNotExist:
            return None

    @property
    def patient_log_url(self) -> str:
        if self.patient_log:
            country = get_current_country(site=self.patient_log.site)
            if country == UGANDA:
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
