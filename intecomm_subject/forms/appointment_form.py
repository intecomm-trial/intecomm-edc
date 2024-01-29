from django import forms
from django.utils.translation import gettext_lazy as _
from edc_appointment.constants import SKIPPED_APPT
from edc_appointment.forms import AppointmentForm as BaseForm
from edc_appointment.models import AppointmentType
from edc_constants.constants import CLINIC, COMMUNITY
from edc_visit_schedule.utils import is_baseline
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.utils import get_assignment_for_subject


class AppointmentForm(BaseForm):
    @property
    def assignment_for_subject(self):
        return get_assignment_for_subject(self.instance.subject_identifier)

    def clean(self):
        cleaned_data = super().clean()
        appt_status = self.cleaned_data.get("appt_status")
        appt_type = self.cleaned_data.get("appt_type")

        # baseline appt_type must match arm
        community_appt_type = AppointmentType.objects.get(name=COMMUNITY)
        facility_appt_type = AppointmentType.objects.get(name=CLINIC)
        if is_baseline(instance=self.instance):
            if (
                appt_type == facility_appt_type
                and self.assignment_for_subject == COMMUNITY_ARM
            ):
                raise forms.ValidationError({"appt_type": _("Invalid. Expected community")})
            elif (
                appt_type == community_appt_type
                and self.assignment_for_subject == FACILITY_ARM
            ):
                raise forms.ValidationError({"appt_type": _("Invalid. Expected facility")})

        # community arm may not skip
        if (
            appt_status
            and appt_status == SKIPPED_APPT
            and self.assignment_for_subject == COMMUNITY_ARM
        ):
            raise forms.ValidationError(
                {"appt_status": _("Invalid. Community appointments may not be skipped")}
            )

        # ensure facility arm does not attend community
        if (
            appt_type
            and appt_type == AppointmentType.objects.get(name=COMMUNITY)
            and self.assignment_for_subject == FACILITY_ARM
        ):
            raise forms.ValidationError(
                {
                    "appt_type": _(
                        "Invalid. A facility-based participant may not attend in the community"
                    )
                }
            )
        return cleaned_data
