from django.db import models
from django_pandas.managers import DataFrameManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_qareports.model_mixins import QaReportModelMixin
from edc_utils import get_utcnow


class BaseVlSummaryModelMixin(
    UniqueSubjectIdentifierFieldMixin, QaReportModelMixin, models.Model
):
    """A modelmixin for VL data management tables with details of each
    HIV participant's viral load value and status.
    """

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
