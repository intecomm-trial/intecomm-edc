from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin

from .view_definition import get_view_definition


class Eos(QaReportModelMixin, DBView):

    visit_datetime = models.DateTimeField(null=True, blank=True)
    timepoint = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    visit_code = models.CharField(max_length=25, null=True)
    visit_code_sequence = models.IntegerField(null=True)
    offstudy_reason = models.CharField(max_length=200, null=True, blank=True)
    offstudy_datetime = models.DateTimeField(null=True, blank=True)
    m = models.IntegerField(verbose_name="months", null=True)
    schedule_status = models.CharField(max_length=25, null=True, blank=True)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "eos_view"
        verbose_name = "End of study"
        verbose_name_plural = "End of study"
