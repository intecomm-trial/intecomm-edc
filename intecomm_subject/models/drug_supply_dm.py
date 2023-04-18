from django.db import models
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import DrugSupplyModelMixin

from intecomm_lists.models import DmTreatments

from .drug_refill_dm import DrugRefillDm


class DrugSupplyDm(DrugSupplyModelMixin, BaseUuidModel):
    drug_refill = models.ForeignKey(DrugRefillDm, on_delete=models.PROTECT)

    drug = models.ForeignKey(DmTreatments, on_delete=models.PROTECT)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Drug Supply: Diabetes"
        verbose_name_plural = "Drug Supply: Diabetes"
