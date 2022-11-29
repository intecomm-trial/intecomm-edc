from django.db import models
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import DrugSupplyModelMixin

from intecomm_lists.models import ArvDrugs

from .drug_refill_hiv import DrugRefillHiv


class DrugSupplyHiv(DrugSupplyModelMixin, BaseUuidModel):

    drug_refill = models.ForeignKey(DrugRefillHiv, on_delete=models.PROTECT)

    drug = models.ForeignKey(ArvDrugs, on_delete=models.PROTECT)

    def __str__(self):
        return self.drug_refill.rx.display_name

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Drug Supply: HIV"
        verbose_name_plural = "Drug Supply: HIV"
