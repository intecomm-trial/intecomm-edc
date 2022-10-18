from django.db import models
from django.utils.html import format_html
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.choices import SELECTION_METHOD, YES_NO
from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import EligibilityModelMixin, ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)

from ..choices import ETHNICITY
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

    selection_method = models.CharField(
        verbose_name="How was the patient selected from the outpatients CTC?",
        max_length=25,
        choices=SELECTION_METHOD,
    )

    hospital_identifier = EncryptedCharField(unique=True, blank=False)

    ethnicity = models.CharField(max_length=15, choices=ETHNICITY)

    qualifying_condition = models.CharField(
        verbose_name=(
            "Has the patient been diagnosis more than 6 months ago with at least one of the "
            "following conditions: HIV, Diabetes and/or Hypertension"
        ),
        max_length=15,
        choices=YES_NO,
    )

    staying_nearby_6 = models.CharField(
        verbose_name=format_html(
            "Is the patient planning to remain in the catchment area "
            "for <u>at least 6 months</u>"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
