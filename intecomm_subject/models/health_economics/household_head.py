from django.utils.translation import gettext_lazy as _
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_he.model_mixins import HouseholdHeadModelMixin, HouseholdModelMixin
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfModelMixin


class HealthEconomicsHouseholdHead(
    SingletonCrfModelMixin,
    HouseholdHeadModelMixin,
    HouseholdModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    # TODO: collapse hoh_ethnicity choices as per last revision (v3)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = _("Health Economics: Household head")
        verbose_name_plural = _("Health Economics: Household head")
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
