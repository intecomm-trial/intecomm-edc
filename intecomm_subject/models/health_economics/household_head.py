from django.db import models
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_he.model_mixins import HouseholdHeadModelMixin, HouseholdModelMixin
from edc_model.models import BaseUuidModel

from ...choices import (
    TZ_ETHNICITY_CHOICES,
    TZ_RELIGION_CHOICES,
    UG_ETHNICITY_CHOICES,
    UG_RELIGION_CHOICES,
)
from ...model_mixins import CrfModelMixin


class HealthEconomicsHouseholdHead(
    SingletonCrfModelMixin,
    HouseholdHeadModelMixin,
    HouseholdModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    hoh_religion = models.CharField(
        verbose_name="How would you describe the household head’s religious orientation?",
        max_length=25,
        choices=UG_RELIGION_CHOICES + TZ_RELIGION_CHOICES,
    )

    hoh_ethnicity = models.CharField(
        verbose_name="What is the household head’s ethnic background?",
        max_length=25,
        choices=UG_ETHNICITY_CHOICES + TZ_ETHNICITY_CHOICES,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Economics: Household head"
        verbose_name_plural = "Health Economics: Household head"
