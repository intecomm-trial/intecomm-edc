from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import HIV, NOT_APPLICABLE
from edc_crf.model_mixins import SingletonCrfModelMixin
from edc_dx_review.model_mixins import rx_initial_review_model_mixin_factory
from edc_dx_review.model_mixins.factory import dx_initial_review_model_mixin_factory
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_reportable import CELLS_PER_MILLIMETER_CUBED_DISPLAY

from ..choices import CARE_ACCESS
from ..model_mixins import CrfModelMixin, ViralLoadResultModelMixin


class HivInitialReview(
    dx_initial_review_model_mixin_factory("dx"),
    rx_initial_review_model_mixin_factory(
        "rx_init", verbose_name_label="antiretroviral therapy (ART)"
    ),
    ViralLoadResultModelMixin,
    SingletonCrfModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    diagnosis_label = HIV

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

    @property
    def best_art_initiation_date(self):
        return self.rx_init_date or self.rx_init_calculated_date

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "HIV Initial Review"
        verbose_name_plural = "HIV Initial Reviews"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
