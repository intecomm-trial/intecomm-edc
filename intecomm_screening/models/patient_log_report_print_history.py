from django.db import models
from edc_model.models import BaseUuidModel
from edc_utils import get_utcnow


class PatientLogReportPrintHistory(BaseUuidModel):
    patient_log_identifier = models.CharField(max_length=25)
    printed_datetime = models.DateTimeField(default=get_utcnow)
    printed_user = models.CharField(max_length=25)

    class Meta(BaseUuidModel.Meta):
        pass
