from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_dx_review.model_mixins.initial_review import InitialReviewModelMixin
from edc_glucose.model_mixins import GlucoseModelMixin
from edc_model import duration_to_date
from edc_model.models import BaseUuidModel, DurationYMDField

from ..choices import DM_MANAGEMENT
from ..model_mixins import CrfModelMixin


class DmInitialReview(
    InitialReviewModelMixin, GlucoseModelMixin, CrfModelMixin, BaseUuidModel
):

    managed_by = models.CharField(
        verbose_name="How is the patient's diabetes managed?",
        max_length=25,
        choices=DM_MANAGEMENT,
        default=NOT_APPLICABLE,
    )

    med_start_ago = DurationYMDField(
        verbose_name=(
            "If the patient is taking medicines for diabetes, "
            "how long have they been taking these?"
        ),
        null=True,
        blank=True,
    )

    med_start_estimated_date = models.DateField(
        verbose_name="Estimated medication start date",
        null=True,
        editable=False,
    )

    med_start_date_estimated = models.CharField(
        verbose_name="Was the medication start date estimated?",
        max_length=15,
        choices=YES_NO,
        default=YES,
        editable=False,
    )

    glucose_performed = models.CharField(
        verbose_name="Has the patient had their glucose measured in the last few months?",
        max_length=15,
        choices=YES_NO,
    )

    def save(self, *args, **kwargs):
        if self.med_start_ago:
            self.med_start_estimated_date = duration_to_date(
                self.med_start_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Diabetes Initial Review"
        verbose_name_plural = "Diabetes Initial Reviews"
