from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NOT_REQUIRED
from edc_constants.constants import NOT_REQUIRED, YES
from edc_model import models as edc_models
from edc_model.models import BaseUuidModel
from edc_vitals.models import (
    DiastolicPressureField,
    HeightField,
    SystolicPressureField,
    WaistCircumferenceField,
    WeightField,
)

from ..model_mixins import CrfModelMixin


class Indicators(CrfModelMixin, BaseUuidModel):
    weight = WeightField(
        validators=[MinValueValidator(25), MaxValueValidator(200)],
        null=True,
        blank=True,
    )

    height = HeightField(
        null=True,
        blank=True,
    )

    waist = WaistCircumferenceField(
        null=True,
        blank=True,
    )

    hip = models.DecimalField(
        verbose_name="Hip circumference:",
        decimal_places=1,
        max_digits=5,
        null=True,
        blank=True,
        help_text="in centimeters",
    )

    r1_taken = models.CharField(
        verbose_name=mark_safe("Was a blood pressure reading taken"),
        max_length=15,
        choices=YES_NO,
        default=YES,
    )

    r1_reason_not_taken = models.TextField(
        verbose_name="reason not taken", max_length=250, null=True, blank=True
    )

    sys_blood_pressure_r1 = SystolicPressureField(null=True, blank=True)

    dia_blood_pressure_r1 = DiastolicPressureField(null=True, blank=True)

    r2_taken = models.CharField(
        verbose_name=mark_safe("Was a <u>second</u> blood pressure reading taken"),
        max_length=15,
        choices=YES_NO_NOT_REQUIRED,
        default=NOT_REQUIRED,
    )

    r2_reason_not_taken = models.TextField(max_length=250, null=True, blank=True)

    sys_blood_pressure_r2 = SystolicPressureField(null=True, blank=True)

    dia_blood_pressure_r2 = DiastolicPressureField(null=True, blank=True)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Indicators"
        verbose_name_plural = "Indicators"
