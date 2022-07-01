from django.db import models
from edc_model import models as edc_models

from intecomm_lists.models import HtnTreatments

from ..model_mixins import DrugSupplyModelMixin
from .drug_refill_htn import DrugRefillHtn


class DrugSupplyHtn(DrugSupplyModelMixin, edc_models.BaseUuidModel):

    drug_refill = models.ForeignKey(DrugRefillHtn, on_delete=models.PROTECT)

    drug = models.ForeignKey(HtnTreatments, on_delete=models.PROTECT)

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Drug Supply: Hypertension"
        verbose_name_plural = "Drug Supply: Hypertension"
