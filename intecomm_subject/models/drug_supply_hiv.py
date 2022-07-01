from django.db import models
from edc_model import models as edc_models

from intecomm_lists.models import ArvDrugs

from ..model_mixins import DrugSupplyModelMixin
from .drug_refill_hiv import DrugRefillHiv


class DrugSupplyHiv(DrugSupplyModelMixin, edc_models.BaseUuidModel):

    drug_refill = models.ForeignKey(DrugRefillHiv, on_delete=models.PROTECT)

    drug = models.ForeignKey(ArvDrugs, on_delete=models.PROTECT)

    def __str__(self):
        return self.drug_refill.rx.display_name

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Drug Supply: HIV"
        verbose_name_plural = "Drug Supply: HIV"
