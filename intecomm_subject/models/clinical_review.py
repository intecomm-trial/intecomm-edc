from edc_dx_review.model_mixins import (
    ClinicalReviewDmModelMixin,
    ClinicalReviewHivModelMixin,
    ClinicalReviewHtnModelMixin,
    ClinicalReviewModelMixin,
)
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class ClinicalReview(
    ClinicalReviewHivModelMixin,
    ClinicalReviewHtnModelMixin,
    ClinicalReviewDmModelMixin,
    ClinicalReviewModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Clinical Review"
        verbose_name_plural = "Clinical Reviews"
