from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_crf.model_mixins import CrfModelMixin
from edc_lab.model_mixins import CrfWithRequisitionModelMixin, requisition_fk_options
from edc_lab_panel.panels import cd4_panel
from edc_model.models import BaseUuidModel
from edc_reportable import (
    CELLS_PER_MILLIMETER_CUBED,
    CELLS_PER_MILLIMETER_CUBED_DISPLAY,
)


class Cd4Result(CrfWithRequisitionModelMixin, CrfModelMixin, BaseUuidModel):

    lab_panel = cd4_panel

    requisition = models.ForeignKey(**requisition_fk_options)

    cd4_value = models.IntegerField(
        verbose_name="CD4 Result",
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text=f"in {CELLS_PER_MILLIMETER_CUBED_DISPLAY}",
    )

    cd4_units = models.CharField(
        verbose_name="Units", max_length=25, default=CELLS_PER_MILLIMETER_CUBED, editable=False
    )

    class Meta(CrfWithRequisitionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "CD4 Result"
        verbose_name_plural = "CD4 Results"
