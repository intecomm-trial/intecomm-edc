from django.db import models

from edc_glucose.model_mixins import (
    fasting_model_mixin_factory,
    fbg_model_mixin_factory,
)
from edc_lab.choices import GLUCOSE_UNITS
from edc_vitals.model_mixins import (
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
)


class FastingModelMixin(
    fasting_model_mixin_factory(),
):
    class Meta:
        abstract = True


class FbgModelMixin(
    fbg_model_mixin_factory(
        "fbg",
        fbg_units=models.CharField(
            verbose_name="FBG units",
            max_length=15,
            choices=GLUCOSE_UNITS,
            null=True,
            blank=True,
        ),
    ),
):
    class Meta:
        abstract = True


class PartTwoFieldsModelMixin(
    FastingModelMixin,
    FbgModelMixin,
    BloodPressureModelMixin,
    SimpleBloodPressureModelMixin,
    models.Model,
):
    part_two_report_datetime = models.DateTimeField(
        verbose_name="Part 2 report date and time",
        null=True,
        blank=False,
        help_text="Date and time of report.",
    )

    class Meta:
        abstract = True
