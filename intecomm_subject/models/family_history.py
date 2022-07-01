from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import TRUE_FALSE_DONT_KNOW
from edc_model import models as edc_models

from ..choices import HOUSEHOLD_YES_NO_CHOICES
from ..model_mixins import CrfModelMixin


class FamilyHistory(CrfModelMixin, edc_models.BaseUuidModel):
    htn_in_household = models.CharField(
        verbose_name=mark_safe(
            "Do you know if anyone else in your household has <u>high blood pressure</u>?"
        ),
        max_length=25,
        choices=HOUSEHOLD_YES_NO_CHOICES,
    )

    dm_in_household = models.CharField(
        verbose_name=mark_safe(
            "Do you know if anyone else in your household has <u>diabetes</u>?"
        ),
        max_length=25,
        choices=HOUSEHOLD_YES_NO_CHOICES,
    )

    hiv_in_household = models.CharField(
        verbose_name=mark_safe("Do you know if anyone else in your household has <u>HIV</u>?"),
        max_length=25,
        choices=HOUSEHOLD_YES_NO_CHOICES,
    )

    high_bp_bs_tf = models.CharField(
        verbose_name=mark_safe(
            "High blood pressure and high blood sugar can cause many "
            "illnesses like heart attacks, stroke, kidney failure"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    overweight_tf = models.CharField(
        verbose_name=mark_safe(
            "Being overweight protects from high blood pressure and high blood sugar"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    salty_foods_tf = models.CharField(
        verbose_name=mark_safe("Salty food protects from high blood sugar"),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    excercise_tf = models.CharField(
        verbose_name=mark_safe(
            "Regular exercise is important for people with <u>high blood "
            "pressure</u> or <u>high blood sugar</u> even if they are taking "
            "medicines for these conditions."
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    take_medicine_tf = models.CharField(
        verbose_name=mark_safe(
            "Drugs for <u>blood sugar</u> and <u>blood pressure</u> can make you unwell"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    stop_htn_meds_tf = models.CharField(
        verbose_name=mark_safe(
            "It is best to stop taking <u>blood pressure</u> pills when "
            "you feel better and start pill taking again when you feel sick"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    traditional_htn_tf = models.CharField(
        verbose_name=mark_safe(
            "Herbs and traditional medicine are better for "
            "managing <u>blood pressure</u> than pills and medicines"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    stop_dm_meds_tf = models.CharField(
        verbose_name=mark_safe(
            "It is best to stop taking <u>blood sugar</u> medicines when "
            "you feel better and start pill taking again when you feel sick"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    traditional_dm_tf = models.CharField(
        verbose_name=mark_safe(
            "Herbs and traditional medicine are better for managing "
            "<u>diabetes</u> than pills and medicines"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    dm_cause_tf = models.CharField(
        verbose_name=mark_safe("Having drinks with sugar (e.g. tea/coffee) causes diabetes"),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Family History and Knowledge"
        verbose_name_plural = "Family History and Knowledge"
