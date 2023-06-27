from django import forms
from django.test import TestCase, tag

from intecomm_screening.tests.intecomm_test_case_mixin import IntecommTestCaseMixin
from intecomm_screening.utils import validate_not_screened_despite_unwilling_to_screen


@tag("scu")
class TestUtils(IntecommTestCaseMixin, TestCase):
    def test_screening_id_not_found_in_patient_log_raises(self):
        patient_log = self.get_patient_log()
        subject_screening = self.get_subject_screening(patient_log=patient_log)
        patient_log.screening_identifier = "some_other_identifier"
        patient_log.save()

        with self.assertRaises(forms.ValidationError) as cm:
            validate_not_screened_despite_unwilling_to_screen(
                subject_screening=subject_screening
            )
        self.assertIn(
            f"Invalid. Patient Log associated with screening identifier "
            f"'{subject_screening.screening_identifier}' not found",
            str(cm.exception),
        )

    def test_multiple_matching_screening_ids_found_in_patient_log_raises(self):
        patient_log = self.get_patient_log()
        subject_screening = self.get_subject_screening(patient_log=patient_log)

        patient_log_two = self.get_patient_log(legal_name="NOTHER AME")
        patient_log_two.screening_identifier = patient_log.screening_identifier
        patient_log_two.save()

        with self.assertRaises(forms.ValidationError) as cm:
            validate_not_screened_despite_unwilling_to_screen(
                subject_screening=subject_screening
            )
        self.assertIn(
            f"Invalid. Multiple Patient Logs associated with screening identifier "
            f"'{subject_screening.screening_identifier}' exist."
            "Inform data manager before continuing.",
            str(cm.exception),
        )
