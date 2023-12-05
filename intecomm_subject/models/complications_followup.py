from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class ComplicationsFollowup(CrfModelMixin, BaseUuidModel):
    # stroke
    stroke = models.CharField(verbose_name="Stroke", max_length=25, choices=YES_NO)

    stroke_date = models.DateField(
        verbose_name="If yes, date",
        null=True,
        blank=True,
        help_text="If exact date not known, see SOP on how to estimate a date.",
    )

    # heart_attack
    heart_attack = models.CharField(
        verbose_name="Heart attack / heart failure",
        max_length=25,
        choices=YES_NO,
    )

    heart_attack_date = models.DateField(
        verbose_name="If yes, date",
        null=True,
        blank=True,
        help_text="If exact date not known, see SOP on how to estimate a date.",
    )

    # renal
    renal_disease = models.CharField(
        verbose_name="Renal (kidney) disease",
        max_length=25,
        choices=YES_NO,
    )

    renal_disease_date = models.DateField(
        verbose_name="If yes, date",
        null=True,
        blank=True,
        help_text="If exact date not known, see SOP on how to estimate a date.",
    )
    # vision
    vision = models.CharField(
        verbose_name="Vision problems (e.g. blurred vision)",
        max_length=25,
        choices=YES_NO,
    )

    vision_date = models.DateField(
        verbose_name="If yes, date",
        null=True,
        blank=True,
        help_text="If exact date not known, see SOP on how to estimate a date.",
    )

    # numbness
    numbness = models.CharField(
        verbose_name="Numbness / burning sensation",
        max_length=25,
        choices=YES_NO,
    )

    numbness_date = models.DateField(
        verbose_name="If yes, date",
        null=True,
        blank=True,
        help_text="If exact date not known, see SOP on how to estimate a date.",
    )

    # foot ulcers
    foot_ulcers = models.CharField(
        verbose_name="Foot ulcers",
        max_length=25,
        choices=YES_NO,
    )

    foot_ulcers_date = models.DateField(
        verbose_name="If yes, date",
        null=True,
        blank=True,
        help_text="If exact date not known, see SOP on how to estimate a date.",
    )
    #
    complications = models.CharField(
        verbose_name="Are there any other major complications to report?",
        max_length=25,
        choices=YES_NO,
        default=NO,
    )

    complications_other = models.TextField(
        null=True,
        blank=True,
        help_text="Please include dates",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Complications: Followup"
        verbose_name_plural = "Complications: Followup"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
