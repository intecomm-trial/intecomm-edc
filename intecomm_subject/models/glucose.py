from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin, GlucoseModelMixin


class Glucose(GlucoseModelMixin, CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Glucose"
        verbose_name_plural = "Glucose"
