from django.db import models
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import DrugRefillModelMixin

from ..model_mixins import CrfModelMixin
from .arv_regimens import ArvRegimens


class DrugRefillHiv(DrugRefillModelMixin, CrfModelMixin, BaseUuidModel):
    rx = models.ForeignKey(
        ArvRegimens,
        verbose_name="Which medicine did the patient receive today?",
        on_delete=models.PROTECT,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Drug Refill: HIV"
        verbose_name_plural = "Drug Refills: HIV"
