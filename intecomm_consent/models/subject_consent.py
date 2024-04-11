from django.contrib.sites.managers import CurrentSiteManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from edc_consent.field_mixins import (
    CitizenFieldsMixin,
    FullNamePersonalFieldsMixin,
    IdentityFieldsMixin,
    ReviewFieldsMixin,
    SampleCollectionFieldsMixin,
    VulnerabilityFieldsMixin,
)
from edc_consent.managers import ConsentObjectsManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import BLACK, NO, NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_identifier.subject_identifier import SubjectIdentifier as BaseSubjectIdentifier
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_screening.utils import (
    get_subject_screening_or_raise,
    validate_screening_identifier_format_or_raise,
)
from edc_sites.model_mixins import SiteModelMixin

from intecomm_screening.utils import raise_if_consent_refusal_exists

from .model_mixins import SearchSlugModelMixin


class SubjectIdentifier(BaseSubjectIdentifier):
    template = "{protocol_number}-{site_id}-{sequence}"
    padding = 4


class SubjectConsent(
    SiteModelMixin,
    ConsentModelMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    NonUniqueSubjectIdentifierModelMixin,
    IdentityFieldsMixin,
    ReviewFieldsMixin,
    FullNamePersonalFieldsMixin,
    SampleCollectionFieldsMixin,
    CitizenFieldsMixin,
    VulnerabilityFieldsMixin,
    SearchSlugModelMixin,
    BaseUuidModel,
):
    """A model completed by the user that captures the ICF."""

    subject_identifier_cls = SubjectIdentifier

    # unique constraint here blocks more than one consent version
    screening_identifier = models.CharField(
        verbose_name="Screening identifier",
        max_length=50,
        unique=True,
        validators=[RegexValidator(r"^[A-Z0-9]+$")],
    )

    screening_datetime = models.DateTimeField(
        verbose_name="Screening datetime", null=True, editable=False
    )

    group_identifier = models.CharField(max_length=50, null=True)

    ethnicity = models.CharField(
        max_length=15,
        help_text="fromm screening",
        editable=False,
        null=True,
        default=BLACK,
    )

    completed_by_next_of_kin = models.CharField(
        max_length=10, default=NO, choices=YES_NO, editable=False
    )

    objects = ConsentObjectsManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords(inherit=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.subject_identifier} v{self.version}"

    def save(self, *args, **kwargs):
        validate_screening_identifier_format_or_raise(self.screening_identifier)
        subject_screening = get_subject_screening_or_raise(self.screening_identifier)
        raise_if_consent_refusal_exists(screening_identifier=self.screening_identifier)
        if not kwargs.get("update_fields"):
            self.screening_datetime = subject_screening.report_datetime
            self.subject_type = "subject"
            self.citizen = NOT_APPLICABLE
        super().save(*args, **kwargs)

    def natural_key(self):
        return self.subject_identifier, self.version

    @property
    def registration_unique_field(self):
        """Required for UpdatesOrCreatesRegistrationModelMixin."""
        return "subject_identifier"

    class Meta(ConsentModelMixin.Meta, BaseUuidModel.Meta):
        constraints = [
            UniqueConstraint(
                fields=["subject_identifier", "version"],
                name="%(app_label)s_%(class)s_subj_ver_uniq",
            ),
            UniqueConstraint(
                fields=[
                    "legal_name",
                    "initials",
                    "version",
                ],
                name="%(app_label)s_%(class)s_legal_name_uniq",
            ),
        ]
        indexes = BaseUuidModel.Meta.indexes + [
            models.Index(
                fields=[
                    "subject_identifier",
                    "legal_name",
                    "dob",
                    "initials",
                    "version",
                ]
            )
        ]
