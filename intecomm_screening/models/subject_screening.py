from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import EligibilityModelMixin, ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

from ..eligibility import ScreeningEligibility


class SubjectScreeningModelError(Exception):
    pass


class ScreeningIdentifier(BaseScreeningIdentifier):

    template = "S{random_string}"


class SubjectScreening(
    EligibilityModelMixin,
    ScreeningModelMixin,
    BaseUuidModel,
):

    identifier_cls = ScreeningIdentifier
    eligibility_cls = ScreeningEligibility

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
