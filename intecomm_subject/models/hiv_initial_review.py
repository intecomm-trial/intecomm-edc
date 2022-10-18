from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_PENDING_NA
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_dx_review.model_mixins.initial_review import InitialReviewModelMixin
from edc_lab.choices import VL_QUANTIFIER_NA
from edc_model import duration_to_date
from edc_model.models import BaseUuidModel, DurationYMDField
from edc_model.validators import date_not_future
from edc_reportable import CELLS_PER_MILLIMETER_CUBED_DISPLAY, COPIES_PER_MILLILITER

from ..choices import CARE_ACCESS
from ..model_mixins import CrfModelMixin


class HivInitialReview(InitialReviewModelMixin, CrfModelMixin, BaseUuidModel):

    receives_care = models.CharField(
        verbose_name="Is the patient receiving care for HIV?",
        max_length=15,
        choices=YES_NO,
    )

    clinic = models.CharField(
        verbose_name="Where does the patient receive care for HIV",
        max_length=15,
        choices=CARE_ACCESS,
        default=NOT_APPLICABLE,
    )

    clinic_other = models.CharField(
        verbose_name="If not attending here, where does the patient attend?",
        max_length=50,
        null=True,
        blank=True,
    )

    arv_initiated = models.CharField(
        verbose_name="Has the patient started antiretroviral therapy (ART)?",
        max_length=15,
        choices=YES_NO,
        default=YES,
    )

    arv_initiation_ago = DurationYMDField(
        verbose_name="How long ago did the patient start ART?",
        null=True,
        blank=True,
        help_text="If possible, provide the exact date below instead of estimating here.",
    )

    arv_initiation_actual_date = models.DateField(
        verbose_name="Date started antiretroviral therapy (ART)",
        validators=[date_not_future],
        null=True,
        help_text="If possible, provide the exact date here instead of estimating above.",
    )

    arv_initiation_estimated_date = models.DateField(
        verbose_name="Estimated Date started antiretroviral therapy (ART)",
        validators=[date_not_future],
        null=True,
        editable=False,
        help_text="Calculated based on response to `arv_initiation_ago`",
    )

    arv_initiation_date_estimated = models.CharField(
        verbose_name="Was the ART start date estimated?",
        max_length=15,
        choices=YES_NO,
        default=YES,
        editable=False,
    )

    # Viral Load
    has_vl = models.CharField(
        verbose_name="Is the patient's most recent viral load result available?",
        max_length=25,
        choices=YES_NO_PENDING_NA,
        default=NOT_APPLICABLE,
    )
    vl = models.IntegerField(
        verbose_name="Most recent viral load",
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=COPIES_PER_MILLILITER,
    )

    vl_quantifier = models.CharField(
        max_length=10,
        choices=VL_QUANTIFIER_NA,
        null=True,
        blank=True,
    )

    vl_date = models.DateField(
        verbose_name="Date of most recent viral load",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    # CD4
    has_cd4 = models.CharField(
        verbose_name="Is the patient's most recent CD4 result available?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    cd4 = models.IntegerField(
        verbose_name="Most recent CD4",
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        null=True,
        blank=True,
        help_text=CELLS_PER_MILLIMETER_CUBED_DISPLAY,
    )

    cd4_date = models.DateField(
        verbose_name="Date of most recent CD4",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.dx_ago:
            self.dx_estimated_date = duration_to_date(self.dx_ago, self.report_datetime)
        if self.arv_initiation_ago:
            self.arv_initiation_estimated_date = duration_to_date(
                self.arv_initiation_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    @property
    def best_art_initiation_date(self):
        return self.arv_initiation_actual_date or self.arv_initiation_estimated_date

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "HIV Initial Review"
        verbose_name_plural = "HIV Initial Reviews"
