from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_dx_review.model_mixins import rx_initial_review_model_mixin_factory
from edc_model.models import BaseUuidModel

from ..model_mixins import (
    CrfModelMixin,
    FollowupReviewModelMixin,
    ViralLoadResultModelMixin,
)


# TODO: Ask for viral load if available since last visit
class HivReview(
    rx_initial_review_model_mixin_factory(
        "rx_init", verbose_name_label="antiretroviral therapy (ART)"
    ),
    ViralLoadResultModelMixin,
    FollowupReviewModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    dx = models.CharField(
        verbose_name="Has the patient been infected with HIV?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    @property
    def best_art_initiation_date(self):
        return self.rx_init_date or self.rx_init_calculated_date

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "HIV Review"
        verbose_name_plural = "HIV Review"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
