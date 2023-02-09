from django.db import models
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import DrugRefillModelMixin

from intecomm_lists.models import DmTreatments

from ..model_mixins import CrfModelMixin


class DrugRefillDm(DrugRefillModelMixin, CrfModelMixin, BaseUuidModel):
    rx = models.ManyToManyField(
        DmTreatments,
        verbose_name="Which medicine did the patient receive today?",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Drug Refill: Diabetes"
        verbose_name_plural = "Drug Refills: Diabetes"
