from edc_constants.constants import COMPLETE, YES
from edc_form_validators import FormValidator

from .patient_group_form_validator import INVALID_RANDOMIZE

INVALID_APPOINTMENT_DATE = "INVALID_APPOINTMENT_DATE"
INVALID_GROUP = "INVALID_GROUP"


class PatientLogFormValidator(FormValidator):
    def clean(self):
        if self.instance.patient_group and self.instance.patient_group.randomized:
            self.raise_validation_error(
                "A patient in a randomized group may not be changed", INVALID_RANDOMIZE
            )
        if (
            self.cleaned_data.get("last_routine_appt_date")
            and self.cleaned_data.get("report_datetime")
            and self.cleaned_data.get("last_routine_appt_date")
            > self.cleaned_data.get("report_datetime").date()
        ):
            self.raise_validation_error(
                {"last_routine_appt_date": "Cannot be a future date"}, INVALID_APPOINTMENT_DATE
            )

        if (
            self.cleaned_data.get("next_routine_appt_date")
            and self.cleaned_data.get("report_datetime")
            and self.cleaned_data.get("next_routine_appt_date")
            < self.cleaned_data.get("report_datetime").date()
        ):
            self.raise_validation_error(
                {"next_routine_appt_date": "Must be a future date"}, INVALID_APPOINTMENT_DATE
            )
        self.required_if(
            YES, field="first_health_talk", field_required="first_health_talk_date"
        )
        self.required_if(
            YES, field="second_health_talk", field_required="second_health_talk_date"
        )

        if from_group := self.instance.patient_group:
            if to_group := self.cleaned_data.get("patient_group"):
                if from_group.id == to_group.id:
                    pass
                elif from_group.status == COMPLETE:
                    self.raise_validation_error(
                        "Cannot remove from current group. Group is complete.", INVALID_GROUP
                    )
                elif to_group.status == COMPLETE:
                    self.raise_validation_error(
                        "Cannot add to group. Group is complete.", INVALID_GROUP
                    )
