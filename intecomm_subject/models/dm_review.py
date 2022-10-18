from edc_glucose.model_mixins import GlucoseModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class DmReview(GlucoseModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes Review"
        verbose_name_plural = "Diabetes Review"
