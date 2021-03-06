from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

from .eligibility_model_mixin import EligibilityModelMixin
from .part_one_fields_model_mixin import PartOneFieldsModelMixin
from .part_two_fields_model_mixin import PartTwoFieldsModelMixin


class SubjectScreeningModelError(Exception):
    pass


class ScreeningIdentifier(BaseScreeningIdentifier):

    template = "S{random_string}"


class SubjectScreening(
    PartOneFieldsModelMixin,
    PartTwoFieldsModelMixin,
    EligibilityModelMixin,
    ScreeningModelMixin,
    BaseUuidModel,
):

    identifier_cls = ScreeningIdentifier

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
