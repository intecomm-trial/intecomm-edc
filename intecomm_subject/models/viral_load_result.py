from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_lab.choices import VL_QUANTIFIER_NA
from edc_lab.constants import EQ
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_reportable import COPIES_PER_MILLILITER

from ..model_mixins import CrfModelMixin


class ViralLoadResult(CrfModelMixin, BaseUuidModel):

    drawn_date = models.DateField(
        verbose_name="Specimen collection date",
        validators=[date_not_future],
    )

    vl_value = models.IntegerField(
        verbose_name="VL Result",
        validators=[MinValueValidator(20), MaxValueValidator(9999999)],
        help_text=f"in {COPIES_PER_MILLILITER}",
    )

    vl_quantifier = models.CharField(max_length=10, choices=VL_QUANTIFIER_NA, default=EQ)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Viral Load Result"
        verbose_name_plural = "Viral Load Results"
