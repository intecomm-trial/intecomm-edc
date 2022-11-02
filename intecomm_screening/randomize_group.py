from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from edc_consent.utils import get_consent_model_cls
from edc_constants.constants import COMPLETE
from edc_screening.utils import get_subject_screening_model_cls
from edc_utils import get_utcnow

if TYPE_CHECKING:
    from .models import PatientGroup


class GroupAlreadyRandomized(Exception):
    pass


class GroupRandomizationError(Exception):
    pass


class RandomizeGroup:
    def __init__(self, instance: PatientGroup):
        self.instance = instance

    def randomize_group(self):
        if self.instance.randomized:
            raise GroupAlreadyRandomized(f"Group is already randomized. Got {self.instance}.")
        if self.instance.status != COMPLETE:
            raise GroupRandomizationError(f"Group is not complete. Got {self.instance}.")
        for patient_log in self.instance.patients.all():
            if not patient_log.screening_identifier:
                raise GroupRandomizationError(
                    f"Patient has not been screened. Got {patient_log}. (1)"
                )
            if not patient_log.subject_identifier:
                raise GroupRandomizationError(
                    f"Patient has not consented. Got {patient_log} (1)."
                )

            # check screening model / eligibility
            self.check_eligibility(patient_log)

            # redundantly check consent model
            try:
                get_consent_model_cls().objects.get(
                    subject_identifier=patient_log.subject_identifier
                )
            except ObjectDoesNotExist:
                raise GroupRandomizationError(
                    f"Patient has not consented. Got {patient_log} (2)."
                )
        return True, get_utcnow(), self.instance.user_modified

    @staticmethod
    def check_eligibility(patient_log):
        try:
            obj = get_subject_screening_model_cls().objects.get(
                subject_identifier=patient_log.screening_identifier
            )
        except ObjectDoesNotExist:
            raise GroupRandomizationError(
                f"Patient has not been screened. Got {patient_log}. (2)"
            )
        else:
            if not obj.eligible:
                raise GroupRandomizationError(f"Patient is not eligible. Got {obj}.")
