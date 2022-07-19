from django.test import TestCase

from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin


class TestSubjectConsent(IntecommTestCaseMixin, TestCase):
    def test_(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)
