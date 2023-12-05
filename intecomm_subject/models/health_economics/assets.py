from django.utils.translation import gettext_lazy as _
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_he.model_mixins import AssetsModelMixin, assets_model_mixin_factory
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfModelMixin


class HealthEconomicsAssets(
    SingletonCrfModelMixin,
    AssetsModelMixin,
    assets_model_mixin_factory(),
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = _("Health Economics: Assets")
        verbose_name_plural = _("Health Economics: Assets")
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
