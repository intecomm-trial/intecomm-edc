from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_constants.choices import YES_NO
from edc_model.models import BaseUuidModel

from intecomm_subject.model_mixins import CrfModelMixin


class ClinicalNote(CrfModelMixin, BaseUuidModel):
    has_comment = models.CharField(
        verbose_name="Are there any aditional comments?",
        max_length=15,
        choices=YES_NO,
    )

    comments = EncryptedTextField(verbose_name="Comments", null=True, blank=True)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Clinical Note"
        verbose_name_plural = "Clinical Note"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
