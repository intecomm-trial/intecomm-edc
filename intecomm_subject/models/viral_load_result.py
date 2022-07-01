from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_lab.choices import VL_QUANTIFIER_NA
from edc_lab.constants import EQ
from edc_model import models as edc_models
from edc_reportable import COPIES_PER_MILLILITER

from ..model_mixins import CrfModelMixin


class ViralLoadResult(CrfModelMixin, edc_models.BaseUuidModel):

    drawn_date = models.DateField(
        verbose_name="Specimen collection date",
        validators=[edc_models.date_not_future],
    )

    result = models.IntegerField(
        verbose_name="VL Result",
        validators=[MinValueValidator(20), MaxValueValidator(9999999)],
        help_text=f"in {COPIES_PER_MILLILITER}",
    )

    quantifier = models.CharField(max_length=10, choices=VL_QUANTIFIER_NA, default=EQ)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Viral Load Result"
        verbose_name_plural = "Viral Load Results"
