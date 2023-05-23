from edc_he.model_mixins import (
    HouseholdHeadModelMixin,
    HouseholdModelMixin,
    PatientModelMixin,
)
from edc_he.model_mixins.factory import assets_model_mixin_factory
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class HealthEconomicsBaseline(
    HouseholdHeadModelMixin,
    HouseholdModelMixin,
    PatientModelMixin,
    assets_model_mixin_factory(),
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Heath economics baseline"
        verbose_name_plural = "Heath economics baseline"
