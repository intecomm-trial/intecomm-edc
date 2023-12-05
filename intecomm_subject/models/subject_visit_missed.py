from django.db import models
from edc_model.models import BaseUuidModel
from edc_visit_tracking.model_mixins import SubjectVisitMissedModelMixin

from intecomm_lists.models import SubjectVisitMissedReasons

from ..model_mixins import CrfWithActionModelMixin


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):
    missed_reasons = models.ManyToManyField(SubjectVisitMissedReasons, blank=True)

    appt_date = models.DateField(
        verbose_name="Next scheduled routine/facility appointment",
        null=True,
        blank=True,
        help_text="Should fall on an Integrated clinic day",
    )

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"
        indexes = CrfWithActionModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
