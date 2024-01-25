from django.db import models
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin

from intecomm_screening.model_mixins import PatientCallModelMixin


class PatientFollowupCall(PatientCallModelMixin, SiteModelMixin, BaseUuidModel):
    patient_log = models.ForeignKey("intecomm_screening.PatientLog", on_delete=models.PROTECT)

    def __str__(self):
        return self.patient_log.subject_identifier

    def natural_key(self):
        return (self.patient_log,)

    natural_key.dependencies = [
        "sites.Site",
        "intecomm_screening.patientlog",
    ]

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Followup Call"
        verbose_name_plural = "Patient Followup Calls"
