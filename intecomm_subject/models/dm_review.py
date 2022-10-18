from django.db import models
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel

from ..choices import DM_MANAGEMENT
from ..model_mixins import CrfModelMixin, GlucoseModelMixin, ReviewModelMixin


class DmReview(ReviewModelMixin, GlucoseModelMixin, CrfModelMixin, BaseUuidModel):

    managed_by = models.CharField(
        verbose_name="How will the patient's diabetes be managed going forward?",
        max_length=25,
        choices=DM_MANAGEMENT,
        default=NOT_APPLICABLE,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes Review"
        verbose_name_plural = "Diabetes Review"
