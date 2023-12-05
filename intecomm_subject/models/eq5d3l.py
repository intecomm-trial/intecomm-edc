from edc_model.models import BaseUuidModel
from edc_qol.model_mixins import Eq5d3lModelMixin

from ..model_mixins import CrfModelMixin


class Eq5d3l(
    Eq5d3lModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(Eq5d3lModelMixin.Meta, CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "EuroQol EQ-5D-3L Instrument"
        verbose_name_plural = "EuroQol EQ-5D-3L Instrument"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
