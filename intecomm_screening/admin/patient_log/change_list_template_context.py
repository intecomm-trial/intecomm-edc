from __future__ import annotations

import re
from typing import TYPE_CHECKING, Type

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from edc_constants.constants import NO, TBD, UUID_PATTERN, YES
from edc_dashboard.url_names import url_names

from ...models import ConsentRefusal
from ...utils import (
    get_consent_refusal_url,
    get_subject_consent_url,
    get_subject_screening_url,
)

if TYPE_CHECKING:
    from intecomm_consent.models import SubjectConsent, SubjectConsentUg

    from ...models import SubjectScreening, SubjectScreeningUg


class ChangeListTemplateContext:
    """Context for change_list_screen_and_consent.html"""

    subject_dashboard_url_name = "subject_dashboard_url"

    def __init__(
        self,
        patient_log,
        subject_screening_model_cls: Type[SubjectScreening | SubjectScreeningUg] = None,
        subject_consent_model_cls: Type[SubjectConsent | SubjectConsentUg] = None,
    ):
        self._consent_refusal = None
        self._eligible = None
        self._randomized = None
        self._screening_identifier = None
        self._subject_consent = None
        self._subject_identifier = None
        self._subject_screening = None
        self.patient_log = patient_log
        self.subject_screening_model_cls = subject_screening_model_cls
        self.subject_consent_model_cls = subject_consent_model_cls

    @property
    def context(self) -> dict:
        """Context for change_list_screen_and_consent.html"""
        return dict(
            TBD=TBD,
            YES=YES,
            NO=NO,
            consent_refusal=self.consent_refusal,
            consent_refusal_url=self.consent_refusal_url,
            eligible=self.eligible,
            filing_identifier=self.patient_log.filing_identifier,
            group_identifier=self.patient_log.group_identifier,
            patient_log_identifier=self.patient_log.patient_log_identifier,
            randomized=self.randomized,
            screening_identifier=self.screening_identifier,
            stable=self.stable,
            subject_consent=self.subject_consent,
            subject_consent_url=self.subject_consent_url,
            subject_dashboard_url=self.subject_dashboard_url,
            subject_identifier=self.subject_identifier,
            subject_screening_url=self.subject_screening_url,
            willing_to_screen=self.patient_log.willing_to_screen,
        )

    @property
    def screening_identifier(self) -> str | None:
        if not self._screening_identifier:
            if re.match(UUID_PATTERN, self.patient_log.screening_identifier):
                self._screening_identifier = None
            else:
                self._screening_identifier = self.patient_log.screening_identifier
        return self._screening_identifier

    @property
    def subject_screening(self) -> SubjectScreening | SubjectScreeningUg | None:
        if not self._subject_screening:
            try:
                self._subject_screening = self.subject_screening_model_cls.objects.get(
                    screening_identifier=self.screening_identifier
                )
            except ObjectDoesNotExist:
                self._subject_screening = None
        return self._subject_screening

    @property
    def consent_refusal(self) -> ConsentRefusal | None:
        if not self._consent_refusal:
            try:
                self._consent_refusal = ConsentRefusal.objects.get(
                    screening_identifier=self.screening_identifier
                )
            except ObjectDoesNotExist:
                pass
        return self._consent_refusal

    @property
    def subject_identifier(self) -> str | None:
        if not self._subject_identifier:
            if re.match(UUID_PATTERN, self.patient_log.subject_identifier):
                self._subject_identifier = None
            else:
                self._subject_identifier = self.patient_log.subject_identifier
        return self._subject_identifier

    @property
    def subject_consent(self):
        if not self._subject_consent:
            try:
                self._subject_consent = self.subject_consent_model_cls.objects.get(
                    screening_identifier=self.screening_identifier
                )
            except ObjectDoesNotExist:
                pass
        return self._subject_consent

    @property
    def eligible(self) -> bool | None:
        """Returns True if patient is screened eligible."""
        if self._eligible is None:
            try:
                self._eligible = self.subject_screening.eligible
            except AttributeError:
                self._eligible = None
        return self._eligible

    @property
    def randomized(self) -> bool | None:
        """Returns True if patient is screened eligible."""
        if self._randomized is None:
            try:
                self._randomized = True if self.patient_log.group_identifier else False
            except AttributeError:
                self._randomized = None
        return self._randomized

    @property
    def stable(self) -> str:
        return (
            self.patient_log.get_stable_display()
            if self.patient_log.stable != TBD
            else TBD.upper()
        )

    @property
    def subject_screening_url(self) -> str | None:
        if self.patient_log.willing_to_screen != YES:
            url = None
        else:
            url = get_subject_screening_url(
                self.patient_log,
                subject_screening=self.subject_screening,
                subject_screening_model_cls=self.subject_screening_model_cls,
            )
        return url

    @property
    def subject_consent_url(self) -> str | None:
        url = None
        if self.subject_screening and self.subject_screening.eligible:
            url = get_subject_consent_url(
                subject_screening=self.subject_screening,
                subject_consent=self.subject_consent,
                subject_consent_model_cls=self.subject_consent_model_cls,
            )
        return url

    @property
    def consent_refusal_url(self) -> str | None:
        url = None
        if self.consent_refusal or (
            self.subject_screening and self.subject_screening.eligible
        ):
            url = get_consent_refusal_url(
                screening_identifier=self.subject_screening.screening_identifier,
                consent_refusal=self.consent_refusal,
            )
        return url

    @property
    def subject_dashboard_url(self) -> str | None:
        url = None
        if self.randomized:
            url = reverse(
                url_names.get(self.subject_dashboard_url_name),
                kwargs=dict(subject_identifier=self.subject_identifier),
            )
        return url
