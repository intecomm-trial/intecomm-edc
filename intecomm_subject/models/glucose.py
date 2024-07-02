from edc_glucose.model_mixins import (
    fasting_model_mixin_factory,
    glucose_model_mixin_factory,
)
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class Glucose(
    glucose_model_mixin_factory("glucose"),
    fasting_model_mixin_factory(
        "glucose",
        verbose_names=dict(
            glucose_fasting="Was glucose measured while fasting?",
            glucose_fasting_duration_str="How long did they fast (in hours and minutes)?",
        ),
    ),
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Glucose"
        verbose_name_plural = "Glucose"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
