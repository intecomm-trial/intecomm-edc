from django.test import TestCase

from intecomm_visit_schedule.visit_schedules import schedule, visit_schedule


class TestVisitSchedule(TestCase):
    def test_visit_schedule_models(self):

        self.assertEqual(visit_schedule.death_report_model, "intecomm_ae.deathreport")
        self.assertEqual(visit_schedule.offstudy_model, "edc_offstudy.subjectoffstudy")
        self.assertEqual(visit_schedule.locator_model, "edc_locator.subjectlocator")

    def test_schedule_models(self):
        self.assertEqual(schedule.onschedule_model, "intecomm_prn.onschedule")
        self.assertEqual(schedule.offschedule_model, "intecomm_prn.endofstudy")
        self.assertEqual(schedule.consent_model, "intecomm_consent.subjectconsent")
        self.assertEqual(schedule.appointment_model, "edc_appointment.appointment")
