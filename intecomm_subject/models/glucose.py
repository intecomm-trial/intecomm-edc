from edc_glucose.model_mixins import GlucoseModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class Glucose(GlucoseModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Glucose"
        verbose_name_plural = "Glucose"
