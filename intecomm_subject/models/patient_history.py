from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_glucose.model_mixins import FastingModelMixin, FbgModelMixin
from edc_model.models import BaseUuidModel
from edc_reportable.units import COPIES_PER_MILLILITER
from edc_vitals.model_mixins import BloodPressureModelMixin
from edc_vitals.models import DiastolicPressureField, SystolicPressureField, WeightField

from ..model_mixins import CrfModelMixin


class PatientHistory(
    CrfModelMixin, BloodPressureModelMixin, FbgModelMixin, FastingModelMixin, BaseUuidModel
):

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
        verbose_name="Systolic pressure", null=True, blank=True
    )

    dia_blood_pressure = DiastolicPressureField(
        verbose_name="Diastolic pressure", null=True, blank=True
    )

    fbg_measured = models.CharField(
        verbose_name="Was the blood sugar measured?",
        max_length=15,
        choices=YES_NO,
        help_text="If yes, indicate below",
    )

    vl_measured = models.CharField(
        verbose_name="Was the viral load measured?",
        max_length=15,
        choices=YES_NO,
        help_text="If yes, indicate below",
    )

    vl_value = models.IntegerField(
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

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "PatientHistory"
        verbose_name_plural = "PatientHistory"
