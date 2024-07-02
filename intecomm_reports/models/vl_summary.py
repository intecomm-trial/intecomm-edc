from django.db import models
from django_pandas.managers import DataFrameManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_qareports.models import QaReportModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow


class VlSummary(
    UniqueSubjectIdentifierFieldMixin, QaReportModelMixin, SiteModelMixin, models.Model
):
    """A data management table with details of each HIV participant's
    viral load.

    """

    report_model = models.CharField(max_length=50, default="intecomm_reports.vlsummary")

    created = models.DateTimeField(default=get_utcnow)

    baseline_date = models.DateField(null=True)

    baseline_vl_date = models.DateField(null=True)

    endline_vl_date = models.DateField(null=True)

    baseline_vl = models.IntegerField(null=True)

    endline_vl = models.IntegerField(null=True)

    objects = DataFrameManager()

    class Meta:
        verbose_name = "Viral load summary"
        verbose_name_plural = "Viral load summary"
