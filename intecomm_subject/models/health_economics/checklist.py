from django.db import models
from django.utils.translation import gettext_lazy as _
from edc_constants.choices import YES_NO
from edc_constants.constants import YES
from edc_model.models import BaseUuidModel

from ...model_mixins import CrfModelMixin


class HealthEconomicsAssets(
    CrfModelMixin,
    BaseUuidModel,
):

    assets = models.CharField(max_length=15, choices=YES_NO, default=YES)
    no_assets_explain = models.TextField(null=True, blank=False)

    income = models.CharField(max_length=15, choices=YES_NO, default=YES)
    no_income_explain = models.TextField(null=True, blank=False)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = _("Health Economics: Checklist")
        verbose_name_plural = _("Health Economics: Checklists")
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
