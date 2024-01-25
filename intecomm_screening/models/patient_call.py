from django.db import models
from edc_constants.constants import NO
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import formatted_date
from edc_utils.date import to_local

from ..model_mixins import PatientCallModelMixin
from .patient_log import PatientLog


class PatientCall(PatientCallModelMixin, SiteModelMixin, BaseUuidModel):
    patient_log = models.ForeignKey(PatientLog, on_delete=models.PROTECT)

    def __str__(self):
        call_again = "Do not call again." if self.call_again == NO else "May call again."
        return f"{formatted_date(to_local(self.report_datetime).date())}. {call_again}"

    def natural_key(self):
        return (self.patient_log,)

    natural_key.dependencies = [
        "sites.Site",
        "intecomm_screening.patientlog",
    ]

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Call"
        verbose_name_plural = "Patient Calls"
