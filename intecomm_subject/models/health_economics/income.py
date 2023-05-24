from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_he.model_mixins import IncomeModelMixin
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfModelMixin


class HealthEconomicsIncome(
    SingletonCrfModelMixin,
    IncomeModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Economics: Income"
        verbose_name_plural = "Health Economics: Income"
