from django.db import models
from edc_model.models import BaseUuidModel
from edc_visit_tracking.constants import VISIT_MISSED_ACTION
from edc_visit_tracking.model_mixins import SubjectVisitMissedModelMixin

from intecomm_lists.models import SubjectVisitMissedReasons

from ..model_mixins import CrfWithActionModelMixin


class SubjectVisitMissed(
    SubjectVisitMissedModelMixin,
    CrfWithActionModelMixin,
    BaseUuidModel,
):
    action_name = VISIT_MISSED_ACTION

    missed_reasons = models.ManyToManyField(SubjectVisitMissedReasons, blank=True)

    class Meta(CrfWithActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Missed Visit Report"
        verbose_name_plural = "Missed Visit Report"
