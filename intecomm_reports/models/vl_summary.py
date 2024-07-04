from django.db import models
from django_pandas.managers import DataFrameManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_qareports.models import QaReportModelMixin
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow


class BaseVlSummary(
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

    offschedule_date = models.DateField(null=True)

    last_vl_date = models.DateField(null=True)

    next_vl_date = models.DateField(null=True)

    expected = models.BooleanField(null=True)

    offset = models.IntegerField(null=True)

    objects = DataFrameManager()

    class Meta:
        abstract = True


class VlSummary(BaseVlSummary):
    class Meta:
        verbose_name = "Viral load summary (endline >= 9m)"
        verbose_name_plural = "Viral load summary (endline >= 9m)"


class VlSummary2(BaseVlSummary):
    class Meta:
        verbose_name = "Viral load summary (endline >= 6m)"
        verbose_name_plural = "Viral load summary (endline >= 6m)"
