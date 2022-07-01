from django.db import models
from edc_model import models as edc_models

from intecomm_lists.models import HtnTreatments

from ..model_mixins import CrfModelMixin, DrugRefillModelMixin


class DrugRefillHtn(DrugRefillModelMixin, CrfModelMixin, edc_models.BaseUuidModel):

    rx = models.ManyToManyField(
        HtnTreatments,
        verbose_name="Which medicine did the patient receive today?",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Drug Refill: Hypertension"
        verbose_name_plural = "Drug Refills: Hypertension"
