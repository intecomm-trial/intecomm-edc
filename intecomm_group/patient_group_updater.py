from __future__ import annotations

from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import DM, HIV, HTN, YES
from intecomm_rando.group_eligibility import assess_group_eligibility
from intecomm_rando.models import RandomizationList
from intecomm_rando.randomize_group import RandomizeGroup
from intecomm_rando.utils import update_patient_in_newly_randomized_group

from .models import PatientGroup

if TYPE_CHECKING:
    from intecomm_consent.models import SubjectConsent
    from intecomm_screening.models import PatientLog, SubjectScreening


class PatientGroupNotRandomized(Exception):
    pass


class PatientGroupUpdaterError(Exception):
    pass


class PatientGroupUpdater:
    def __init__(self, patient_group: PatientGroup, subject_identifier: str):
        self.group_name: str = patient_group.name
        self.subject_identifier = subject_identifier
        self.patient_group = patient_group
        if not patient_group.randomized:
            raise PatientGroupNotRandomized(
                f"PatientGroup has not been randomized. Got {self.group_name}."
            )
        self.patient_log: PatientLog = self.get_patient_log_or_raise(subject_identifier)
        if self.patient_group.patients.filter(id=self.patient_log.id).exists():
            raise PatientGroupUpdaterError(
                f"{self.subject_identifier} already in group {self.group_name}."
            )
        elif self.patient_log.group_identifier:
            patient_group = PatientGroup.objects.get(
                group_identifier=self.patient_log.group_identifier
            )
            raise PatientGroupUpdaterError(
                f"{self.subject_identifier} already in "
                f"group {patient_group.name} / {self.patient_log.group_identifier}."
            )
        self.subject_screening: SubjectScreening = self.get_subject_screening_or_raise(
            subject_identifier
        )
        self.subject_consent_exists_or_raise(subject_identifier)

    def add_subject_to_group(self):
        # add to patient to group
        for condition in self.conditions:
            if condition == HIV:
                self.patient_group.hiv_patients.add(self.patient_log)
            elif condition == HTN:
                self.patient_group.htn_patients.add(self.patient_log)
            elif condition == DM:
                self.patient_group.dm_patients.add(self.patient_log)
            else:
                raise PatientGroupUpdaterError(
                    f"Unknown condition. See {self.subject_identifier}. Got {condition}."
                )
            self.patient_group.patients.add(self.patient_log)
        self.patient_group.save()
        self.patient_group.refresh_from_db()
        assess_group_eligibility(self.patient_group, called_by_rando=True)
        randomize_group = RandomizeGroup(self.patient_group)
        randomize_group._update_all_for_one_patient(self.patient_log)
        rando_obj = RandomizationList.objects.get(
            group_identifier=self.patient_group.group_identifier
        )
        update_patient_in_newly_randomized_group(
            self.patient_log, rando_obj.assignment, rando_obj.allocated_datetime
        )

    @property
    def patient_log_model_cls(self) -> PatientLog:
        return django_apps.get_model("intecomm_screening.patientlog")

    @property
    def subject_screening_model_cls(self) -> SubjectScreening:
        return django_apps.get_model("intecomm_screening.subjectscreening")

    @property
    def subject_consent_model_cls(self) -> SubjectConsent:
        return django_apps.get_model("intecomm_consent.subjectconsent")

    def get_patient_log_or_raise(self, subject_identifier: str) -> PatientLog:
        """Returns the patient log or raises"""
        try:
            patient_log = self.patient_log_model_cls.objects.get(
                subject_identifier=subject_identifier
            )
        except ObjectDoesNotExist:
            raise PatientGroupUpdaterError(
                f"{self.patient_log_model_cls._meta.verbose_name} does not "
                f"exist. Got {subject_identifier}."
            )
        return patient_log

    def get_subject_screening_or_raise(self, subject_identifier: str) -> SubjectScreening:
        """Returns subject screening or raises."""
        try:
            subject_screening = self.subject_screening_model_cls.objects.get(
                subject_identifier=subject_identifier
            )
        except ObjectDoesNotExist:
            raise PatientGroupUpdaterError(
                f"{self.subject_screening_model_cls._meta.verbose_name} does not "
                f"exist. Got {subject_identifier}."
            )
        return subject_screening

    def subject_consent_exists_or_raise(self, subject_identifier) -> None:
        try:
            self.subject_consent_model_cls.objects.get(subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            raise PatientGroupUpdaterError(
                f"{self.subject_consent_model_cls._meta.verbose_name} does not "
                f"exist. Got {subject_identifier}."
            )

    @property
    def conditions(self) -> list[str]:
        conditions_screen = []
        if self.subject_screening.dm_dx == YES:
            conditions_screen.append(DM)
        if self.subject_screening.hiv_dx == YES:
            conditions_screen.append(HIV)
        if self.subject_screening.htn_dx == YES:
            conditions_screen.append(HTN)
        conditions_screen.sort()
        condition_log = [
            obj.name for obj in self.patient_log.conditions.all().order_by("name")
        ]
        if not condition_log or not conditions_screen:
            raise PatientGroupUpdaterError(
                f"No chronic conditions reported. See {self.patient_log.subject_identifier}. "
            )
        elif condition_log != conditions_screen:
            raise PatientGroupUpdaterError(
                f"Inconsistent chronic conditions reported. See "
                f"{self.patient_log.subject_identifier}. "
                f"Got {conditions_screen} != {condition_log}."
            )
        return conditions_screen
