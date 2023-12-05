from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_adverse_event.model_mixins import DeathReportModelMixin
from edc_constants.choices import YES_NO
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from ..choices import DEATH_LOCATIONS, INFORMANT_RELATIONSHIP
from ..pdf_reports import DeathPdfReport


class DeathReport(DeathReportModelMixin, BaseUuidModel):
    pdf_report_cls = DeathPdfReport

    study_day = models.IntegerField(default=0, editable=False, help_text="not used")

    cause_of_death = models.TextField(
        verbose_name="Main cause of death",
        help_text=(
            "Main cause of death in the opinion of the local study doctor and local PI"
        ),
        null=True,
        blank=False,
    )

    death_location = models.CharField(
        verbose_name="Where did the participant die?",
        max_length=50,
        choices=DEATH_LOCATIONS,
    )

    hospital_name = models.CharField(
        verbose_name=(
            "If death occurred at hospital / clinic, please give name of the facility"
        ),
        max_length=150,
        null=True,
        blank=True,
    )

    informant_contact = EncryptedTextField(null=True, blank=True)

    informant_relationship = models.CharField(
        max_length=50,
        choices=INFORMANT_RELATIONSHIP,
        verbose_name="Informants relationship to the participant?",
    )

    other_informant_relationship = OtherCharField()

    death_certificate = models.CharField(
        verbose_name="Is a death certificate is available?",
        max_length=15,
        choices=YES_NO,
    )

    class Meta(DeathReportModelMixin.Meta, BaseUuidModel.Meta):
        indexes = DeathReportModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
