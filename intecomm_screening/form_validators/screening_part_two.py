from django import forms
from edc_form_validators import FormValidator

from ..eligibility.eligibility_part_two import EligibilityPartTwo


class ScreeningPartTwoFormValidator(FormValidator):
    def clean(self):
        pass

    @property
    def eligible_part_two(self) -> bool:
        """Returns False if any of the required fields is YES."""
        eligibility = EligibilityPartTwo(cleaned_data=self.cleaned_data)
        return eligibility.is_eligible

    def raise_if_not_future_appt_datetime(self):
        """Raises if appt_datetime is not future relative to
        part_two_report_datetime.
        """
        appt_datetime = self.cleaned_data.get("appt_datetime")
        report_datetime = self.cleaned_data.get("part_two_report_datetime")
        if appt_datetime and report_datetime:
            tdelta = appt_datetime - report_datetime

            hours = tdelta.seconds / 3600

            if (tdelta.days == 0 and hours < 10) or tdelta.days < 0:
                raise forms.ValidationError(
                    {
                        "appt_datetime": (
                            f"Invalid date. Must be at least 10hrs "
                            f"from report date/time. Got {tdelta.days} "
                            f"days {round(hours, 1)} hrs."
                        )
                    }
                )
