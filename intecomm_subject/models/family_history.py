from django.db import models
from edc_constants.choices import TRUE_FALSE_DONT_KNOW
from edc_model.models import BaseUuidModel

from ..choices import HOUSEHOLD_YES_NO_CHOICES
from ..model_mixins import CrfModelMixin


class FamilyHistory(CrfModelMixin, BaseUuidModel):
    htn_in_household = models.CharField(
        verbose_name="Do you know if anyone else in your household has high blood pressure?",
        max_length=25,
        choices=HOUSEHOLD_YES_NO_CHOICES,
    )

    dm_in_household = models.CharField(
        verbose_name="Do you know if anyone else in your household has diabetes?",
        max_length=25,
        choices=HOUSEHOLD_YES_NO_CHOICES,
    )

    hiv_in_household = models.CharField(
        verbose_name="Do you know if anyone else in your household has HIV?",
        max_length=25,
        choices=HOUSEHOLD_YES_NO_CHOICES,
    )

    high_bp_bs_tf = models.CharField(
        verbose_name=(
            "High blood pressure and high blood sugar can cause many "
            "illnesses like heart attacks, stroke, kidney failure"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    overweight_tf = models.CharField(
        verbose_name=(
            "Being overweight protects from high blood pressure and high blood sugar"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    salty_foods_tf = models.CharField(
        verbose_name="Salty food protects from high blood sugar",
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    excercise_tf = models.CharField(
        verbose_name=(
            "Regular exercise is important for people with high blood "
            "pressure or high blood sugar even if they are taking "
            "medicines for these conditions."
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    take_medicine_tf = models.CharField(
        verbose_name="Drugs for blood sugar and blood pressure can make you unwell",
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    stop_htn_meds_tf = models.CharField(
        verbose_name=(
            "It is best to stop taking blood pressure pills when "
            "you feel better and start pill taking again when you feel sick"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    traditional_htn_tf = models.CharField(
        verbose_name=(
            "Herbs and traditional medicine are better for "
            "managing blood pressure than pills and medicines"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    stop_dm_meds_tf = models.CharField(
        verbose_name=(
            "It is best to stop taking blood sugar medicines when "
            "you feel better and start pill taking again when you feel sick"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    traditional_dm_tf = models.CharField(
        verbose_name=(
            "Herbs and traditional medicine are better for managing "
            "diabetes than pills and medicines"
        ),
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    dm_cause_tf = models.CharField(
        verbose_name="Having drinks with sugar (e.g. tea/coffee) causes diabetes",
        max_length=25,
        choices=TRUE_FALSE_DONT_KNOW,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Family History and Knowledge"
        verbose_name_plural = "Family History and Knowledge"
