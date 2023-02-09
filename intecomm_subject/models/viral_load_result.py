from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_lab.choices import VL_QUANTIFIER_NA
from edc_lab.constants import EQ
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_panel.panels import vl_panel
from edc_model.models import BaseUuidModel
from edc_reportable import COPIES_PER_MILLILITER

from ..model_mixins import CrfModelMixin


class ViralLoadResult(CrfWithRequisitionModelMixin, CrfModelMixin, BaseUuidModel):
    lab_panel = vl_panel

    requisition = models.ForeignKey(
        limit_choices_to={"panel__name": vl_panel.name}, **requisition_fk_options
    )

    vl_value = models.IntegerField(
        verbose_name="VL Result",
        validators=[MinValueValidator(20), MaxValueValidator(9999999)],
        help_text=f"in {COPIES_PER_MILLILITER}",
    )

    vl_quantifier = models.CharField(
        verbose_name="Quantifier", max_length=10, choices=VL_QUANTIFIER_NA, default=EQ
    )

    vl_units = models.CharField(
        verbose_name="Units", max_length=25, default=COPIES_PER_MILLILITER, editable=False
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Viral Load Result"
        verbose_name_plural = "Viral Load Results"
