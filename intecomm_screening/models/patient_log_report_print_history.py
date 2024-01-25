from django.db import models
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow


class PatientLogReportPrintHistory(SiteModelMixin, BaseUuidModel):
    patient_log_identifier = models.CharField(max_length=36)
    printed_datetime = models.DateTimeField(default=get_utcnow)
    printed_user = models.CharField(max_length=25)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Log Report Print History"
        verbose_name_plural = "Patient Log Report Print History"
