from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab.constants import EQ
from edc_model import models as edc_models
from edc_reportable.units import COPIES_PER_MILLILITER
from edc_vitals.models import DiastolicPressureField, SystolicPressureField, WeightField

from intecomm_lists.models import VisitReasons

from ..choices import GLUCOSE_UNITS
from ..model_mixins import CrfModelMixin


class PatientHistory(CrfModelMixin, edc_models.BaseUuidModel):
    visit_reason = models.ManyToManyField(
        VisitReasons,
        verbose_name="Reason for this visit",
    )

    new_complaints = models.CharField(
        verbose_name="Does the patient have any new complaints on this visit?",
        max_length=15,
        choices=YES_NO,
    )

    new_complaints_detail = models.TextField(
        verbose_name="If yes, provide detail",
        max_length=250,
        null=True,
        blank=True,
    )

    weight_measured = models.CharField(
        verbose_name="Was the weight measured??",
        max_length=15,
        choices=YES_NO,
        help_text="If yes, indicate below",
    )

    weight = WeightField(
        null=True,
        blank=True,
    )

    bp_measured = models.CharField(
        verbose_name="Was the blood pressure measured?",
        max_length=15,
        choices=YES_NO,
        help_text="If yes, indicate below",
    )

    sys_blood_pressure = SystolicPressureField(
        verbose_name="Reading 1: Systolic pressure", null=True, blank=True
    )

    dia_blood_pressure = DiastolicPressureField(
        verbose_name="Reading 1: Diastolic pressure", null=True, blank=True
    )

    glucose_measured = models.CharField(
        verbose_name="Was the blood sugar measured?",
        max_length=15,
        choices=YES_NO,
        help_text="If yes, indicate below",
    )

    # IFG
    fasted = models.CharField(
        verbose_name="Has the participant fasted?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )
    fasting_glucose = models.DecimalField(
        verbose_name=mark_safe("Fasting glucose <u>level</u>"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fasting_glucose_quantifier = models.CharField(
        max_length=10,
        choices=RESULT_QUANTIFIER,
        default=EQ,
    )

    fasting_glucose_units = models.CharField(
        verbose_name="Units (fasting glucose)",
        max_length=15,
        choices=GLUCOSE_UNITS,
        blank=True,
        null=True,
    )

    vl_measured = models.CharField(
        verbose_name="Was the viral load measured?",
        max_length=15,
        choices=YES_NO,
        help_text="If yes, indicate below",
    )

    viral_load = models.IntegerField(
        verbose_name="Last viral load",
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        null=True,
        blank=True,
        help_text=COPIES_PER_MILLILITER,
    )

    counseling = models.CharField(
        verbose_name="Did the patient receive health education/counselling?",
        max_length=15,
        choices=YES_NO,
    )

    out_refrral = models.CharField(
        verbose_name="Was there an Out-referral?",
        max_length=15,
        choices=YES_NO,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "PatientHistory"
        verbose_name_plural = "PatientHistory"
