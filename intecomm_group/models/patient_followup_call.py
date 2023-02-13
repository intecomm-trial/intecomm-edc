from django.db import models
from edc_constants.constants import NO, YES
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin
from edc_utils import formatted_date

from intecomm_screening.model_mixins import PatientCallModelMixin


class PatientFollowupCall(PatientCallModelMixin, SiteModelMixin, BaseUuidModel):
    patient_log = models.ForeignKey("intecomm_screening.PatientLog", on_delete=models.PROTECT)

    def __str__(self):
        report_dt = formatted_date(self.report_datetime.date())
        call_again = "Do not call" if self.call_again == NO else "Call again"
        if self.call_again == YES:
            msg = (
                f"{report_dt}: {self.patient_log} was last called "
                f"{self.report_datetime}. {call_again}."
            )
        else:
            msg = f"{report_dt}: {self.patient_log}."
        return msg

    def natural_key(self):
        return (self.patient_log,)

    natural_key.dependencies = [
        "sites.Site",
        "intecomm_screening.patientlog",
    ]

    class Meta:
        verbose_name = "Patient Followup Call"
        verbose_name_plural = "Patient Followup Calls"
        ordering = ["report_datetime"]
