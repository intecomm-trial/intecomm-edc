from edc_dx_review.model_mixins.factory import baseline_review_model_mixin_factory
from edc_model.models import BaseUuidModel
from edc_rx.model_mixins import TreatmentPayMethodsModelMixin
from edc_visit_schedule.constants import DAY1

from ..model_mixins import CrfModelMixin


class ClinicalReviewBaselineError(Exception):
    pass


class ClinicalReviewBaseline(
    TreatmentPayMethodsModelMixin,
    baseline_review_model_mixin_factory(),
    CrfModelMixin,
    BaseUuidModel,
):
    def save(self, *args, **kwargs):
        if (
            self.subject_visit.visit_code != DAY1
            and self.subject_visit.visit_code_sequence != 0
        ):
            raise ClinicalReviewBaselineError(
                f"This form is only available at baseline. Got `{self.subject_visit}`. "
                "Perhaps catch this in the form."
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Clinical Review: Baseline"
        verbose_name_plural = "Clinical Review: Baseline"
