from django.db import models
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import DrugSupplyModelMixin

from intecomm_lists.models import HtnTreatments

from .drug_refill_htn import DrugRefillHtn


class DrugSupplyHtn(DrugSupplyModelMixin, BaseUuidModel):
    drug_refill = models.ForeignKey(DrugRefillHtn, on_delete=models.PROTECT)

    drug = models.ForeignKey(HtnTreatments, on_delete=models.PROTECT)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Drug Supply: Hypertension"
        verbose_name_plural = "Drug Supply: Hypertension"
