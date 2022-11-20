from django.db import models
from edc_model.models import BaseUuidModel

from intecomm_lists.models import HtnTreatments

from ..model_mixins import CrfModelMixin, DrugRefillModelMixin


class DrugRefillHtn(DrugRefillModelMixin, CrfModelMixin, BaseUuidModel):

    rx = models.ManyToManyField(
        HtnTreatments,
        verbose_name="Which medicine did the patient receive today?",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Drug Refill: Hypertension"
        verbose_name_plural = "Drug Refills: Hypertension"
