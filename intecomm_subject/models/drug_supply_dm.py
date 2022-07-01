from django.db import models
from edc_model import models as edc_models

from intecomm_lists.models import DmTreatments

from ..model_mixins import DrugSupplyModelMixin
from .drug_refill_dm import DrugRefillDm


class DrugSupplyDm(DrugSupplyModelMixin, edc_models.BaseUuidModel):

    drug_refill = models.ForeignKey(DrugRefillDm, on_delete=models.PROTECT)

    drug = models.ForeignKey(DmTreatments, on_delete=models.PROTECT)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Drug Supply: Diabetes"
        verbose_name_plural = "Drug Supply: Diabetes"
