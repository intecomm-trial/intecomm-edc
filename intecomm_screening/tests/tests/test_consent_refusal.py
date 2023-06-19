from django.test import TestCase, tag

from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_screening.utils import AlreadyRefusedConsentError


@tag("cr")
class TestConsentRefusal(IntecommTestCaseMixin, TestCase):
    def test_consent_refusal_ok(self):
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        consent_refusal = self.get_consent_refusal(subject_screening=subject_screening)
        self.assertEqual(
            consent_refusal.screening_identifier,
            subject_screening.screening_identifier,
        )

    def test_refusing_consent_more_than_once_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(subject_screening=subject_screening)

        with self.assertRaises(AlreadyRefusedConsentError) as cm:
            self.get_consent_refusal(subject_screening=subject_screening)
        self.assertIn(
            "Patient has already refused consent. "
            f"See {subject_screening.screening_identifier}.",
            str(cm.exception),
        )

    def test_refusing_consent_then_consenting_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(subject_screening=subject_screening)

        with self.assertRaises(AlreadyRefusedConsentError) as cm:
            self.get_subject_consent(subject_screening)
        self.assertIn(
            "Patient has already refused consent. "
            f"See {subject_screening.screening_identifier}.",
            str(cm.exception),
        )
