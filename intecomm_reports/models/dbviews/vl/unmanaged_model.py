from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions
from edc_utils import get_utcnow

from .view_definition import get_view_definition


class Vl(QaReportModelMixin, DBView):
    """A data management table with details of each HIV participant's
    viral load.
    """

    report_model = models.CharField(max_length=50, default="intecomm_reports.vl")

    created = models.DateTimeField(default=get_utcnow)

    vl_value = models.IntegerField(null=True)

    baseline_date = models.DateField(null=True)

    vl_date = models.DateField(null=True)

    m = models.IntegerField(verbose_name="months", null=True)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "intecomm_reports_vl_view"
        verbose_name = "Viral loads"
        verbose_name_plural = "Viral loads"
        default_permissions = qa_reports_permissions
