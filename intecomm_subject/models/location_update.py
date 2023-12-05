from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_constants.choices import YES_NO
from edc_constants.constants import CLINIC, COMMUNITY, OTHER
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from intecomm_subject.model_mixins import CrfModelMixin


class LocationUpdate(CrfModelMixin, BaseUuidModel):
    location = models.CharField(
        verbose_name="Where is this visit taking place",
        choices=(
            (COMMUNITY, "In the community"),
            (CLINIC, "At the facility"),
            (OTHER, "Other, specify below ..."),
        ),
        max_length=100,
    )

    location_other = OtherCharField()

    comments = EncryptedTextField(
        verbose_name=(
            "Briefly explain why the participant is not at the location expected "
            "based on their randomization"
        ),
    )

    next_location = models.CharField(
        verbose_name=(
            "Is the participant expected to attend their next visit at the "
            "location they were randomized to"
        ),
        choices=YES_NO,
        max_length=15,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Location update"
        verbose_name_plural = "Location updates"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
