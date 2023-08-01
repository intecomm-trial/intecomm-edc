from edc_model.models import BaseUuidModel
from edc_qol.model_mixins import IcecapaModelMixin

from ..model_mixins import CrfModelMixin


class Icecapa(
    IcecapaModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(IcecapaModelMixin.Meta, CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Overall quality of life (ICECAP-A V2)"
        verbose_name_plural = "Overall quality of life (ICECAP-A V2)"
