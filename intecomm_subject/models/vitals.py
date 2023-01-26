from django.db import models
from edc_model import models as edc_models
from edc_vitals.model_mixins import BloodPressureModelMixin
from edc_vitals.models import (
    HeartRateField,
    HeightField,
    RespiratoryRateField,
    TemperatureField,
    WaistCircumferenceField,
    WeightField,
)

from ..choices import EST_MEASURED_CHOICES
from ..model_mixins import CrfModelMixin


class Vitals(
    BloodPressureModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):

    weight = WeightField(null=True)

    weight_determination = models.CharField(
        verbose_name="Is weight estimated or measured?",
        max_length=15,
        choices=EST_MEASURED_CHOICES,
    )

    heart_rate = HeartRateField()

    respiratory_rate = RespiratoryRateField(null=True, blank=True)

    temperature = TemperatureField()

    height = HeightField(null=True, blank=True)

    waist = WaistCircumferenceField(null=True, blank=True)

    hip = models.DecimalField(
        verbose_name="Hip circumference:",
        decimal_places=1,
        max_digits=5,
        null=True,
        blank=True,
        help_text="in centimeters",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Vitals"
        verbose_name_plural = "Vitals"
