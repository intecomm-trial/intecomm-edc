from django.contrib.sites.models import Site
from django.db import models
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField
from edc_constants.choices import YES_NO_TBD
from edc_constants.constants import TBD
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators.phone import phone_number
from edc_model_fields.fields import InitialsField
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from intecomm_lists.models import Conditions


class PatientLogManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class PatientLog(SiteModelMixin, BaseUuidModel):

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

    name = EncryptedCharField(blank=False, unique=True)

    initials = InitialsField()

    report_datetime = models.DateTimeField(default=get_utcnow)

    site = models.ForeignKey(
        Site,
        verbose_name="Health facility",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="+",
    )

    hf_identifier = EncryptedCharField(
        verbose_name="Health facility identifier",
        unique=True,
        blank=False,
        help_text="Must be unique",
    )

    contact_number = EncryptedCharField(null=True, blank=False, validators=[phone_number])

    alt_contact_number = EncryptedCharField(null=True, blank=True, validators=[phone_number])

    may_contact = models.CharField(
        verbose_name="Has the patient agreed to be contacted prior to consent?",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
    )

    location_description = EncryptedTextField(
        null=True, blank=True, help_text="Street, landmarks near home, etc"
    )

    patient_group = models.ForeignKey(
        "intecomm_screening.PatientGroup",
        verbose_name="Choose a group (RECOMMENDED)",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text=(
            "This can be changed at anytime until the group is flagged as COMPLETE. "
            "It is recommended to choose a group early in the process."
        ),
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

    last_routine_appt_date = models.DateField(
        verbose_name="When was the patient last seen at this health facility",
        null=True,
        blank=True,
        help_text=(
            "If known, the last appointment may help to estimate the next appointment or "
            "the expected frequency of routine appointments"
        ),
    )

    next_routine_appt_date = models.DateField(
        verbose_name=(
            "When is the patient next scheduled for a routine "
            "appointment at this health facility"
        ),
        null=True,
        blank=True,
        help_text="If known, this date will help prioritize efforts to contact the patient",
    )

    first_health_talk = models.CharField(
        verbose_name="Attended general INTECOMM health talk",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
    )

    first_health_talk_date = models.DateField(
        null=True,
        blank=True,
    )

    second_health_talk = models.CharField(
        verbose_name="Attended INTECOMM sensitisation session",
        max_length=15,
        choices=YES_NO_TBD,
        default=TBD,
    )

    second_health_talk_date = models.DateField(
        verbose_name="Sensitisation session date", null=True, blank=True
    )

    on_site = CurrentSiteManager()

    objects = PatientLogManager()

    history = HistoricalRecords(inherit=True)

    def __str__(self):
        grp = " <available>" if not self.patient_group else f" @ {self.patient_group.name}"
        return f"{self.name.title()} ({self.initials.upper()}){grp}"

    def natural_key(self):
        return (self.name,)  # noqa


class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
    verbose_name = "Patient Log"
    verbose_name_plural = "Patient Log"
