from edc_model import models as edc_models
from edc_visit_schedule.constants import DAY1

from ..model_mixins import (
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewModelMixin,
    CrfModelMixin,
    TreatmentPayMethodsModelMixin,
)


class ClinicalReviewBaselineError(Exception):
    pass


class ClinicalReviewBaseline(
    TreatmentPayMethodsModelMixin,
    ClinicalReviewBaselineHivModelMixin,
    ClinicalReviewBaselineHtnModelMixin,
    ClinicalReviewBaselineDmModelMixin,
    ClinicalReviewModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    def save(self, *args, **kwargs):
        if (
            self.subject_visit.visit_code != DAY1
            and self.subject_visit.visit_code_sequence != 0
        ):
            raise ClinicalReviewBaselineError(
                f"This model is only valid at baseline. Got `{self.subject_visit}`."
            )
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Review: Baseline"
        verbose_name_plural = "Clinical Review: Baseline"
