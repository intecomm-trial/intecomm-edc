from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.choices import YES_NO
from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import EligibilityModelMixin, ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)


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

    screening_consent = models.CharField(
        verbose_name=(
            "Has the subject given his/her verbal consent "
            "to be screened for the INTECOMM trial?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    hospital_identifier = EncryptedCharField(unique=True, blank=False)

    lives_nearby = models.CharField(
        verbose_name="Is the patient living within the catchment population of the facility",
        max_length=15,
        choices=YES_NO,
    )

    staying_nearby_12 = models.CharField(
        verbose_name=(
            "Is the patient planning to remain in the catchment area for at least 12 months"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
