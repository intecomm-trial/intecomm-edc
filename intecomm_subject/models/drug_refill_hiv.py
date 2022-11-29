from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import DrugRefillModelMixin

from ..model_mixins import CrfModelMixin
from .arv_regimens import ArvRegimens


class DrugRefillHiv(DrugRefillModelMixin, CrfModelMixin, BaseUuidModel):

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

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Drug Refill: HIV"
        verbose_name_plural = "Drug Refills: HIV"
