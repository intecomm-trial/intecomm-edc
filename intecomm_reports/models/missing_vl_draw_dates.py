from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin
from edc_utils import get_utcnow


class MissingVlDrawDates(QaReportModelMixin, models.Model):
    report_model = models.CharField(
        max_length=50, default="intecomm_reports.missingvldrawdates"
    )

    created = models.DateTimeField(default=get_utcnow)

    baseline_date = models.DateField(null=True)

    visit_date = models.DateField(null=True)

    visit_code = models.FloatField(null=True)

    vl = models.IntegerField(null=True)

    objects = models.Manager()

    class Meta:
        db_table = "intecomm_reports_missingvldrawdates"
        verbose_name = "Viral load: Missing draw date"
        verbose_name_plural = "Viral load: Missing draw dates"
