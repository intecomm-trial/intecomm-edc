from edc_dx_review.model_mixins import (
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewModelMixin,
)
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import TreatmentPayMethodsModelMixin
from edc_visit_schedule.constants import DAY1

from ..model_mixins import CrfModelMixin


class ClinicalReviewBaselineError(Exception):
    pass


class ClinicalReviewBaseline(
    TreatmentPayMethodsModelMixin,
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    def save(self, *args, **kwargs):
        if (
            self.subject_visit.visit_code != DAY1
            and self.subject_visit.visit_code_sequence != 0
        ):
            raise ClinicalReviewBaselineError(
                f"This model is only valid at baseline. Got `{self.subject_visit}`. "
                "Perhaps cathc this in the form."
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Clinical Review: Baseline"
        verbose_name_plural = "Clinical Review: Baseline"
