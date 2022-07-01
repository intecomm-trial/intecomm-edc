from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin, DrugRefillModelMixin
from .proxy_models import ArvRegimens


class DrugRefillHiv(DrugRefillModelMixin, CrfModelMixin, edc_models.BaseUuidModel):

    rx = models.ForeignKey(
        ArvRegimens,
        verbose_name="Which medicine did the patient receive today?",
        on_delete=models.PROTECT,
    )

    clinic_days = models.IntegerField(
        verbose_name="How many days supplied by the clinic",
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        help_text="days",
    )

    club_days = models.IntegerField(
        verbose_name="How many days supplied by a club",
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        help_text="days",
    )

    purchased_days = models.IntegerField(
        verbose_name="How many days supplied by to be purchased",
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        help_text=(
            "This can be purchased by patient, through a medicines club "
            "that the patient belong to, through insurance or someone else has paid. "
        ),
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Drug Refill: HIV"
        verbose_name_plural = "Drug Refills: HIV"
