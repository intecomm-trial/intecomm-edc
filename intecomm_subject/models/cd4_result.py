from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model import models as edc_models
from edc_reportable import CELLS_PER_MILLIMETER_CUBED_DISPLAY

from ..model_mixins import CrfModelMixin


class Cd4Result(CrfModelMixin, edc_models.BaseUuidModel):

    drawn_date = models.DateField(
        verbose_name="Specimen collection date",
        validators=[edc_models.date_not_future],
    )

    result = models.IntegerField(
        verbose_name="CD4 Result",
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text=f"in {CELLS_PER_MILLIMETER_CUBED_DISPLAY}",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "CD4 Result"
        verbose_name_plural = "CD4 Results"
