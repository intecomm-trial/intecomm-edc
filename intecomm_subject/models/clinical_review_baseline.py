from edc_dx_review.model_mixins import (
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewBaselineModelMixin,
)
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class ClinicalReviewBaseline(
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Clinical Review: Baseline"
        verbose_name_plural = "Clinical Review: Baseline"
