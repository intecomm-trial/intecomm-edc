from django.urls import reverse
from django.utils.html import format_html
from edc_constants.constants import COMPLETE, YES
from edc_form_validators import FormValidator

INVALID_PATIENT_COUNT = "INVALID_PATIENT_COUNT"
INVALID_RANDOMIZE = "INVALID_RANDOMIZE"
INVALID_PATIENT = "INVALID_PATIENT"


class PatientGroupFormValidator(FormValidator):
    def clean(self):
        if self.instance.randomized:
            self.raise_validation_error(
                "A randomized group may not be changed", INVALID_RANDOMIZE
            )
        # confirm at least 8 if complete
        if (
            self.cleaned_data.get("status") == COMPLETE
            and self.cleaned_data.get("patients").count() < 8
        ):
            self.raise_validation_error(
                {"status": "Invalid. Must have at least 8 patients"}, INVALID_PATIENT_COUNT
            )

        # confirm complete cannot be changed if randomized
        if self.cleaned_data.get("status") != COMPLETE and self.instance.randomized:
            self.raise_validation_error(
                {"status": "Invalid. Group has already been randomized"}, INVALID_RANDOMIZE
            )
        if self.cleaned_data.get("randomize") != YES and self.instance.randomized:
            self.raise_validation_error(
                {"randomize": "Invalid. Group has already been randomized"}, INVALID_RANDOMIZE
            )

        # confirm complete before randomize == YES
        if (
            self.cleaned_data.get("status") != COMPLETE
            and self.cleaned_data.get("randomize") == YES
        ):
            self.raise_validation_error(
                {"randomize": "Invalid. Group is not complete"}, INVALID_RANDOMIZE
            )

        if self.cleaned_data.get("status") == COMPLETE:
            self.review_patients()

    def review_patients(self):
        for patient in self.cleaned_data.get("patients"):
            if patient.stable != YES:
                patient_log_url = reverse(
                    "intecomm_screening_admin:intecomm_screening_patientlog_change",
                    args=(patient.id,),
                )
                errmsg = format_html(
                    "Patient is not known to be stable and in-care. "
                    f'See <a href="{patient_log_url}">{patient}</a>'
                )
                self.raise_validation_error(errmsg, INVALID_PATIENT)
