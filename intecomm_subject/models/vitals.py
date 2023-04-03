from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NO
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

from ..choices import ESTIMATED_MEASURED_CHOICES
from ..model_mixins import CrfModelMixin


class Vitals(
    BloodPressureModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    weight = WeightField(null=True, blank=True)

    weight_determination = models.CharField(
        verbose_name="Is weight estimated or measured?",
        max_length=15,
        choices=ESTIMATED_MEASURED_CHOICES,
    )

    bp_one_taken = models.CharField(
        "Was the first blood pressure reading done",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    bp_one_not_taken_reason = models.CharField(
        "If not done, please explain", max_length=50, null=True, blank=True
    )

    bp_two_taken = models.CharField(
        "Was the second blood pressure reading done",
        max_length=15,
        choices=YES_NO_NA,
        null=True,
        blank=False,
    )

    bp_two_not_taken_reason = models.CharField(
        "If not done, please explain", max_length=50, null=True, blank=True
    )

    severe_htn = models.CharField(
        verbose_name="Does the patient have severe hypertension?",
        max_length=15,
        choices=YES_NO_NA,
        help_text="Based on the above readings. Severe HTN is any BP reading > 180/110mmHg",
        default=NO,
    )

    heart_rate = HeartRateField(null=True, blank=True)

    respiratory_rate = RespiratoryRateField(null=True, blank=True)

    temperature = TemperatureField(null=True, blank=True)

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

    comments = models.TextField(null=True, blank=True)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Vitals"
        verbose_name_plural = "Vitals"
