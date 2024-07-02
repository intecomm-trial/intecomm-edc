from django.db import models
from edc_qareports.models import QaReportModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow


class Vl(QaReportModelMixin, SiteModelMixin, models.Model):
    """A data management table with details of each HIV participant's
    viral load.

    """

    report_model = models.CharField(max_length=50, default="intecomm_reports.vl")

    created = models.DateTimeField(default=get_utcnow)

    vl_value = models.IntegerField(null=True)

    baseline_date = models.DateField(null=True)

    vl_date = models.DateField(null=True)

    m = models.IntegerField(verbose_name="months", null=True)

    class Meta:
        managed = False
        db_table = "intecomm_reports_vl_view"
        verbose_name = "Viral loads"
        verbose_name_plural = "Viral loads"
