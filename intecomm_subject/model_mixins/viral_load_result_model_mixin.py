from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO_PENDING_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_lab.choices import VL_QUANTIFIER_NA
from edc_model.validators import date_not_future
from edc_reportable import COPIES_PER_MILLILITER


class ViralLoadResultModelMixin(models.Model):
    # Viral Load
    has_vl = models.CharField(
        verbose_name="Is the patient's most recent viral load result available?",
        max_length=25,
        choices=YES_NO_PENDING_NA,
        default=NOT_APPLICABLE,
        help_text="",
    )

    vl = models.IntegerField(
        verbose_name="Most recent viral load",
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=COPIES_PER_MILLILITER,
    )

    vl_quantifier = models.CharField(
        max_length=10,
        choices=VL_QUANTIFIER_NA,
        null=True,
        default=NOT_APPLICABLE,
    )

    drawn_date = models.DateField(
        verbose_name="Date specimen drawn",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="If exact date not known, please estimate",
    )

    class Meta:
        abstract = True
