from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_he.model_mixins import (
    AssetsModelMixin,
    HouseholdHeadModelMixin,
    HouseholdModelMixin,
    IncomeModelMixin,
    PatientModelMixin,
    PropertyModelMixin,
    assets_model_mixin_factory,
)
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class HealthEconomicsBaseline(
    SingletonCrfModelMixin,
    HouseholdHeadModelMixin,
    HouseholdModelMixin,
    PatientModelMixin,
    AssetsModelMixin,
    assets_model_mixin_factory(),
    PropertyModelMixin,
    IncomeModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Heath economics baseline"
        verbose_name_plural = "Heath economics baseline"
