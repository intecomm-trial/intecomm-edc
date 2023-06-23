from django.test import TestCase, tag

from intecomm_consent.utils import AlreadyConsentedError
from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_screening.utils import AlreadyRefusedConsentError


@tag("sc")
class TestSubjectConsent(IntecommTestCaseMixin, TestCase):
    def test_consent_ok(self):
        subject_screening = self.get_subject_screening()
        self.assertEqual(subject_screening.reasons_ineligible, None)
        self.assertTrue(subject_screening.eligible)

        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)

    def test_consenting_more_than_once_raises(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)

        with self.assertRaises(AlreadyConsentedError) as cm:
            self.get_subject_consent(subject_screening)
        self.assertIn(
            f"Subject has already consented. See {subject_consent.subject_identifier}.",
            str(cm.exception),
        )

    def test_consenting_after_refusing_consent_raises(self):
        subject_screening = self.get_subject_screening()
        self.get_consent_refusal(subject_screening=subject_screening)

        with self.assertRaises(AlreadyRefusedConsentError) as cm:
            self.get_subject_consent(subject_screening)
        self.assertIn(
            "Patient has already refused consent. "
            f"See {subject_screening.screening_identifier}.",
            str(cm.exception),
        )
