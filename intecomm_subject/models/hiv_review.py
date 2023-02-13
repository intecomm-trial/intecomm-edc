from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin, FollowupReviewModelMixin


class HivReview(FollowupReviewModelMixin, CrfModelMixin, BaseUuidModel):
    dx = models.CharField(
        verbose_name="Has the patient been infected with HIV?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    arv_initiated = models.CharField(
        verbose_name="Has the patient started antiretroviral therapy (ART)?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="Select `not applicable` if previously reported.",
    )
    arv_initiation_actual_date = models.DateField(
        verbose_name="Date started antiretroviral therapy (ART)",
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "HIV Review"
        verbose_name_plural = "HIV Review"
