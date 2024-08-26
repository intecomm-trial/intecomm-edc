from django.db import models

from .model_mixins import BaseVlSummaryModelMixin


class VlSummary9m(BaseVlSummaryModelMixin):
    """A data management table to list expected VL results
    for baseline and endline.

    See class VlSummary. For example, to populate:
        vl_summary = VlSummary(endline_months=9, skip_update_dx=True)

    Populated in the modeladmin.get_queryset
    """

    report_model = models.CharField(max_length=50, default="intecomm_reports.vlsummary6m")

    class Meta:
        verbose_name = "Viral load summary (endline >= 9m)"
        verbose_name_plural = "Viral load summary (endline >= 9m)"


class VlSummary6m(BaseVlSummaryModelMixin):
    """A data management table to list expected VL results
    for baseline and endline.

    See class VlSummary. For example, to populate:
        vl_summary = VlSummary(endline_months=6, skip_update_dx=True)

    Populated in the modeladmin.get_queryset
    """

    report_model = models.CharField(max_length=50, default="intecomm_reports.vlsummary9m")

    class Meta:
        verbose_name = "Viral load summary (endline >= 6m)"
        verbose_name_plural = "Viral load summary (endline >= 6m)"
