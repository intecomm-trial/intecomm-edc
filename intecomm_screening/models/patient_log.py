from __future__ import annotations

import re

from django.apps import apps as django_apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.html import format_html
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField
from edc_consent.utils import get_remove_patient_names_from_countries
from edc_constants.choices import GENDER, YES_NO_TBD
from edc_constants.constants import DM, HIV, HTN, TBD, UUID_PATTERN
from edc_model.models import BaseUuidModel, HistoricalRecords, NameFieldsModelMixin
from edc_model.validators.phone import phone_number
from edc_model_fields.fields import InitialsField, OtherCharField
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin
from edc_sites.site import sites
from edc_utils import get_utcnow, get_uuid

from intecomm_lists.models import Conditions, ScreeningRefusalReasons

from ..identifiers import FilingIdentifier, PatientLogIdentifier
from ..utils import validate_screening_identifier, validate_subject_identifier
from .proxy_models import Site


class PatientLogManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, legal_name):
        return self.get(legal_name=legal_name)


class PatientLog(SiteModelMixin, NameFieldsModelMixin, BaseUuidModel):
    filing_identifier = models.CharField(
        verbose_name="Filing number",
        max_length=36,
        blank=True,
        unique=True,
        help_text=format_html(
            "Auto-populated when form is saved. <BR>"
            "This is a sequential-like identifier to label this patient's paper file"
        ),
    )
    patient_log_identifier = models.CharField(
        verbose_name="Patient Log Reference",
        max_length=36,
        unique=True,
        blank=True,
        help_text=format_html(
            "Auto-populated when form is saved. <BR>"
            "You may prefer to use the FILING NUMBER. <BR>"
            "This identifier is replaced by the 'screening identifier' if the patient screens "
            "for the INTECOMM trial"
        ),
    )

    screening_identifier = models.CharField(
        max_length=36,
        default=get_uuid,
        unique=True,
        help_text="Auto populated when screening form is complete",
    )

    screening_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Auto populated when screening form is complete",
    )

    subject_identifier = models.CharField(
        max_length=36,
        default=get_uuid,
        unique=True,
        help_text="Auto populated when consent form is complete",
    )

    consent_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Auto populated when consent form is complete",
    )

    group_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        help_text="Auto populated when group is randomized",
    )

    initials = InitialsField()

    gender = models.CharField(choices=GENDER, max_length=10, blank=False)

    age_in_years = models.IntegerField(
        verbose_name="Age",
        validators=[MinValueValidator(18), MaxValueValidator(110)],
    )

    report_datetime = models.DateTimeField(default=get_utcnow)

    site = models.ForeignKey(
        Site,
        verbose_name="Which site is this?",
        on_delete=models.PROTECT,
        blank=False,
        help_text="This question is asked to confirm you are logged in to the correct site.",
    )

    hospital_identifier = EncryptedCharField(
        verbose_name="Hospital identifier",
        unique=True,
        blank=False,
        help_text="Must be unique",
    )

    last_4_hospital_identifier = EncryptedCharField(
        verbose_name="Last 4 digits of hospital_identifier",
        null=True,
        editable=False,
        help_text="auto-populated",
    )

    contact_number = EncryptedCharField(
        blank=False, validators=[phone_number], help_text="If unknown, type 'UNKNOWN'"
    )

    alt_contact_number = EncryptedCharField(null=True, blank=True, validators=[phone_number])

    last_4_contact_number = EncryptedCharField(
        verbose_name="Last 4 digits of contact number",
        null=True,
        editable=False,
        help_text="auto-populated",
    )

    may_contact = models.CharField(
        verbose_name="Has the patient agreed to be contacted prior to consent?",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
    )

    location_description = EncryptedTextField(
        null=True, blank=True, help_text="Street, landmarks near home, etc"
    )

    conditions = models.ManyToManyField(
        Conditions,
        limit_choices_to={"name__in": [HIV, DM, HTN]},
        verbose_name="Diagnoses",
    )

    stable = models.CharField(
        verbose_name="Do the facility health care staff consider the patient stable in care",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
        help_text="Refer to the SOP for the definition of 'stable'.",
    )

    last_appt_date = models.DateField(
        verbose_name="When was the patient last seen at this health facility",
        null=True,
        blank=True,
        help_text=(
            "If known, the last appointment may help to estimate the next appointment or "
            "the expected frequency of routine appointments"
        ),
    )

    next_appt_date = models.DateField(
        verbose_name="Next scheduled routine appointment at this health facility",
        null=True,
        blank=True,
        help_text="If known, this date will help prioritize efforts to contact the patient",
    )

    first_health_talk = models.CharField(
        verbose_name="Attended general health talk",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
    )

    first_health_talk_date = models.DateField(
        verbose_name="General talk date",
        null=True,
        blank=True,
    )

    second_health_talk = models.CharField(
        verbose_name="Attended sensitisation session",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
    )

    second_health_talk_date = models.DateField(
        verbose_name="Sensitisation session date", null=True, blank=True
    )

    call_attempts = models.IntegerField(default=0, help_text="auto-updated", blank=True)

    willing_to_screen = models.CharField(
        verbose_name="Has the patient agreed to be screened for the INTECOMM study",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
    )

    screening_refusal_reason = models.ForeignKey(
        ScreeningRefusalReasons,
        on_delete=models.PROTECT,
        verbose_name="Reason subject unwilling to screen",
        null=True,
        blank=False,
    )

    screening_refusal_reason_other = OtherCharField()

    printed = models.BooleanField(default=False)

    comment = models.CharField(max_length=250, null=True, blank=True)

    objects = PatientLogManager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords(inherit=True)

    def __str_safe__(self):
        g = "G" if self.group_identifier else ""
        return (
            f"{self.patient_log_identifier} {self.age_in_years}{self.gender} "
            f"({self.site.id}){g}"
        )

    def __str__(self):
        remove_patient_names = False
        g = "G" if self.group_identifier else ""
        for country in get_remove_patient_names_from_countries():
            if self.site and self.site.id in [
                s.site_id for s in sites.get_by_country(country, aslist=True)
            ]:
                remove_patient_names = True
                break
        if remove_patient_names or re.match(UUID_PATTERN, str(self.legal_name)):
            return format_html(
                f"{self.filing_identifier} {self.initials} "
                f"{self.age_in_years}{self.gender} ({self.site.id}){g}"
            )
        return format_html(
            f"{self.legal_name.upper()}-{self.contact_number[-4:]} {self.initials} "
            f"{self.age_in_years}{self.gender} ({self.site.id}){g}"
        )

    def save(self, *args, **kwargs):
        if not kwargs.get("update_fields"):
            if not re.match(UUID_PATTERN, str(self.legal_name or "")):
                self.legal_name = self.legal_name.upper()
            if not re.match(UUID_PATTERN, str(self.familiar_name or "")):
                self.familiar_name = self.familiar_name.upper()
            self.initials = self.initials.upper()
            self.last_4_contact_number = self.contact_number[-4:]
            self.last_4_hospital_identifier = self.hospital_identifier[-4:]
            if not self.filing_identifier or re.match(
                UUID_PATTERN, str(self.filing_identifier)
            ):
                self.filing_identifier = FilingIdentifier(site_id=self.site.id).identifier
            if not self.patient_log_identifier or re.match(
                UUID_PATTERN, str(self.patient_log_identifier)
            ):
                self.patient_log_identifier = PatientLogIdentifier().identifier
        validate_screening_identifier(
            self.screening_identifier,
            subject_screening_model_cls=self.subject_screening_model_cls,
            calling_model=self,
        )
        validate_subject_identifier(
            self.subject_identifier,
            subject_consent_model_cls=self.subject_consent_model_cls,
            calling_model=self,
        )
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.legal_name,)  # noqa

    @property
    def patient_group(self):
        return self.patientgroup_set.all().first()

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model("intecomm_screening.subjectscreening")

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model("intecomm_consent.subjectconsent")

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Log"
        verbose_name_plural = "Patient Log"
        constraints = [
            UniqueConstraint(
                fields=["legal_name", "initials"], name="%(app_label)s_%(class)s_legal_n_uniq"
            )
        ]
