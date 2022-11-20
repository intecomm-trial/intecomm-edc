from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import format_html
from edc_lab.constants import EQ
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_reportable import PERCENT

from ..model_mixins import CrfModelMixin


class Hba1cResult(CrfModelMixin, BaseUuidModel):

    drawn_date = models.DateField(
        verbose_name="Specimen collection date",
        validators=[date_not_future],
    )

    result = models.DecimalField(
        verbose_name="Result",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(20.0)],
        help_text=f"in {PERCENT}",
    )

    quantifier = models.CharField(
        verbose_name=format_html("HbA1c quantifier"),
        max_length=10,
        default=EQ,
    )

    units = models.CharField(
        verbose_name="HbA1c units", max_length=15, default=PERCENT, editable=False
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "HbA1c Result"
        verbose_name_plural = "HbA1c Results"
