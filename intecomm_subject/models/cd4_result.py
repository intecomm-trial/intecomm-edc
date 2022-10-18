from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_reportable import CELLS_PER_MILLIMETER_CUBED_DISPLAY

from ..model_mixins import CrfModelMixin


class Cd4Result(CrfModelMixin, BaseUuidModel):

    drawn_date = models.DateField(
        verbose_name="Specimen collection date",
        validators=[date_not_future],
    )

    result = models.IntegerField(
        verbose_name="CD4 Result",
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text=f"in {CELLS_PER_MILLIMETER_CUBED_DISPLAY}",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "CD4 Result"
        verbose_name_plural = "CD4 Results"
