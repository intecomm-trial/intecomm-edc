from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_lab.choices import RESULT_QUANTIFIER_NA
from edc_model.validators import date_not_future

from intecomm_subject.choices import GLUCOSE_UNITS


class GlucoseModelMixin(models.Model):
    glucose_date = models.DateField(
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    glucose_fasted = models.CharField(
        verbose_name="Had the participant fasted?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    glucose = models.DecimalField(
        verbose_name=mark_safe("Glucose result"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    glucose_quantifier = models.CharField(
        max_length=10,
        choices=RESULT_QUANTIFIER_NA,
        default=NOT_APPLICABLE,
    )

    glucose_units = models.CharField(
        verbose_name="Units (glucose)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        default=NOT_APPLICABLE,
    )

    class Meta:
        abstract = True
