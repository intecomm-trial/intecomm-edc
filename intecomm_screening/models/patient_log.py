from __future__ import annotations

from uuid import uuid4

from django.db import models
from django.utils.html import format_html
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField
from edc_constants.choices import GENDER, YES_NO_TBD
from edc_constants.constants import DM, HIV, HTN, TBD
from edc_model.models import BaseUuidModel, HistoricalRecords, NameFieldsModelMixin
from edc_model.validators.phone import phone_number
from edc_model_fields.fields import InitialsField
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from intecomm_lists.models import Conditions

from .proxy_models import Site


class PatientLogManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, legal_name):
        return self.get(legal_name=legal_name)


def abbrev_cond(c: list | None) -> str:
    c = sorted(c, key=str.casefold)
    if c == [DM]:
        abbrev = "*d*"
    elif c == [DM, HIV]:
        abbrev = "hd*"
    elif c == [DM, HTN]:
        abbrev = "*dt"
    elif c == [DM, HIV, HTN]:
        abbrev = "hdt"
    elif c == [HIV]:
        abbrev = "h**"
    elif c == [HIV, HTN]:
        abbrev = "h*t"
    elif c == [HTN]:
        abbrev = "**t"
    elif not c:
        abbrev = "***"
    else:
        raise TypeError(f"Invalid list of conditions. Got c == {c}.")
    return abbrev


class PatientLog(SiteModelMixin, NameFieldsModelMixin, BaseUuidModel):

    patient_log_identifier = models.CharField(
        max_length=36,
        default=uuid4,
        unique=True,
    )

    screening_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        help_text="Auto populated when screening form is complete",
    )

    screening_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Auto populated when screening form is complete",
    )

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        help_text="Auto populated when consent form is complete",
    )

    consent_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Auto populated when consent form is complete",
    )

    initials = InitialsField()

    gender = models.CharField(choices=GENDER, max_length=10, blank=False)

    age_in_years = models.IntegerField(verbose_name="Age")

    report_datetime = models.DateTimeField(default=get_utcnow)

    site = models.ForeignKey(
        Site,
        verbose_name="Health center",
        on_delete=models.PROTECT,
        blank=False,
        related_name="+",
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
        help_text="This date will help prioritize efforts to contact the patient",
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

    on_site = CurrentSiteManager()
    objects = PatientLogManager()
    history = HistoricalRecords()

    def __str__(self):
        return format_html(f"{self.legal_name.upper()}-{self.contact_number[-4:]}")

    def save(self, *args, **kwargs):
        self.legal_name = self.legal_name.upper()
        self.familiar_name = self.familiar_name.upper()
        self.initials = self.initials.upper()
        self.last_4_contact_number = self.contact_number[-4:]
        self.last_4_hospital_identifier = self.hospital_identifier[-4:]
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.legal_name,)  # noqa

    @property
    def patient_group(self):
        return self.patientgroup_set.all().first()


class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
    verbose_name = "Patient Log"
    verbose_name_plural = "Patient Log"
