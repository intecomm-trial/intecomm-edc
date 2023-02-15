from django.test import tag
from edc_appointment.models import Appointment

from intecomm_group.models import PatientGroup
from intecomm_group.tests.test_case_mixin import TestCaseMixin
from intecomm_screening.models import PatientLog, SubjectScreening


class TestBaselineCrfs(TestCaseMixin):
    def setUp(self):
        patients = self.get_patients(
            dm=6, htn=6, hiv=5, stable=True, screen=True, consent=True
        )
        patient_logs = PatientLog.objects.filter(id__in=[obj.id for obj in patients])
        patient_group = self.get_patient_group(patient_logs)
        self.patient_group = self.randomize_patient_group(patient_group)

    def randomize_next_group(self, name: str) -> PatientGroup:
        patients = self.get_patients(
            dm=6, htn=6, hiv=5, stable=True, screen=True, consent=True
        )
        patient_logs = PatientLog.objects.filter(id__in=[obj.id for obj in patients])
        patient_group = self.get_patient_group(patient_logs, name=name)
        return self.randomize_patient_group(patient_group)

    def test_patient_group_comm_ok(self):
        self.assertEqual(
            self.patient_group.patients.filter(subject_identifier__isnull=True).count(), 0
        )

        qs = SubjectScreening.objects.filter(
            eligible=True,
            screening_identifier__in=[
                obj.screening_identifier for obj in self.patient_group.patients.all()
            ],
        )
        # all eligible in group
        self.assertEqual(self.patient_group.patients.all().count(), qs.count())

        patient_log = self.patient_group.patients.all()[0]
        appointments = Appointment.objects.filter(
            subject_identifier=patient_log.subject_identifier
        )

        # appts have been created
        self.assertGreater(appointments.count(), 0)

        # based on test randomization list in intecomm_edc/tests/etc
        self.assertEqual(appointments[0].schedule_name, "comm_schedule")

        # assumes a monthly schedule for comm
        self.assertEqual(len([o.visit_code for o in appointments]), 13)

    @tag("1")
    def test_patient_group_clinic_ok(self):
        patient_group = self.randomize_next_group(name="GROUP2")
        patient_log = patient_group.patients.all()[0]
        appointments = Appointment.objects.filter(
            subject_identifier=patient_log.subject_identifier
        )

        # based on test randomization list in intecomm_edc/tests/etc
        self.assertEqual(appointments[0].schedule_name, "inte_schedule")

        # assumes a baseline and 12m for inte
        self.assertEqual(len([o.visit_code for o in appointments]), 2)
