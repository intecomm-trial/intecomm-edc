from __future__ import annotations

import re

from edc_constants.constants import TBD, UUID_PATTERN
from intecomm_rando.exceptions import GroupRandomizationError

from intecomm_screening.models import PatientLog

from ..test_case_mixin import TestCaseMixin


class TestPatientGroup(TestCaseMixin):
    def test_randomize_group_ok(self):
        patients = self.get_patients(
            dm=10, htn=0, hiv=4, stable=True, screen=True, consent=True
        )
        patient_logs = PatientLog.objects.filter(id__in=[obj.id for obj in patients])

        patient_group = self.get_patient_group(patient_logs)

        patient_group = self.randomize_patient_group(patient_group)

        # assert group identifier set
        self.assertIsNotNone(patient_group.group_identifier)
        if re.match(UUID_PATTERN, patient_group.group_identifier):
            self.fail("Patient group identifier not set. Unexpectedly got UUID")

        # assert group identfier updated on patient log
        # (updated by randomize_group)
        self.assertEqual(
            PatientLog.objects.filter(group_identifier=patient_group.group_identifier).count(),
            14,
        )

        # assert patient log important identifiers have been set up
        for patient_log in PatientLog.objects.filter(
            group_identifier=patient_group.group_identifier
        ):
            self.assertIsNotNone(patient_log.screening_identifier)
            self.assertIsNotNone(patient_log.subject_identifier)
            self.assertIsNotNone(patient_log.group_identifier)

    def test_randomize_group_not_ready_ineligible(self):
        patients = self.get_patients(
            dm=10, htn=0, hiv=4, stable=True, screen=True, consent=True
        )

        # change one patient to not stable
        # (this would not be possible by a user since the patient has
        # already consented)
        patients[0].stable = TBD
        patients[0].save()
        patient_logs = PatientLog.objects.filter(id__in=[obj.id for obj in patients])

        patient_group = self.get_patient_group(patient_logs)

        # one patient in group is not stable
        with self.assertRaises(GroupRandomizationError) as cm:
            self.randomize_patient_group(patient_group)
        self.assertIn("Patient is not known to be stable", str(cm.exception))

    def test_randomize_group_not_ready_consented(self):
        patients = self.get_patients(
            dm=10, htn=0, hiv=4, stable=True, screen=True, consent=False
        )
        patient_logs = PatientLog.objects.filter(id__in=[obj.id for obj in patients])

        patient_group = self.get_patient_group(patient_logs)

        # patients have not consented
        with self.assertRaises(GroupRandomizationError) as cm:
            self.randomize_patient_group(patient_group)
        self.assertIn("Patient has not consented", str(cm.exception))
