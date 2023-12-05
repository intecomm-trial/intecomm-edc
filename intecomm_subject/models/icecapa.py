from edc_model.models import BaseUuidModel
from edc_qol.model_mixins import IcecapaModelMixin

from ..model_mixins import CrfModelMixin


class Icecapa(
    IcecapaModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(IcecapaModelMixin.Meta, CrfModelMixin.Meta, BaseUuidModel.Meta):
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
