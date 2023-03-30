from django.db import models
from edc_constants.choices import YES_NO
from edc_dx_review.model_mixins import (
    ClinicalReviewDmModelMixin,
    ClinicalReviewHivModelMixin,
    ClinicalReviewHtnModelMixin,
)
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import TreatmentPayMethodsModelMixin

from ..model_mixins import ClinicalReviewModelMixin, CrfModelMixin


class ClinicalReview(
    ClinicalReviewHivModelMixin,
    ClinicalReviewHtnModelMixin,
    ClinicalReviewDmModelMixin,
    TreatmentPayMethodsModelMixin,
    ClinicalReviewModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    complications = models.CharField(
        verbose_name="Since last seen, has the patient had any complications",
        max_length=15,
        choices=YES_NO,
        help_text="If Yes, complete the `Complications` CRF",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Clinical Review"
        verbose_name_plural = "Clinical Reviews"
