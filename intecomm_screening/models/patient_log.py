from uuid import uuid4

from django.contrib.sites.models import Site
from django.db import models
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField
from edc_constants.choices import GENDER, YES_NO_TBD
from edc_constants.constants import NEW, TBD
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators.phone import phone_number
from edc_model_fields.fields import InitialsField
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow
from intecomm_form_validators import RECRUITING

from intecomm_lists.models import Conditions


class PatientLogManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class PatientLog(SiteModelMixin, BaseUuidModel):

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

    name = EncryptedCharField(blank=False, unique=True)

    initials = InitialsField()

    gender = models.CharField(choices=GENDER, max_length=10, blank=False)

    report_datetime = models.DateTimeField(default=get_utcnow)

    site = models.ForeignKey(
        Site,
        verbose_name="Health facility",
        on_delete=models.PROTECT,
        blank=False,
        related_name="+",
    )

    hf_identifier = EncryptedCharField(
        verbose_name="Health facility identifier",
        unique=True,
        blank=False,
        help_text="Must be unique",
    )

    contact_number = EncryptedCharField(
        blank=False, validators=[phone_number], help_text="If unknown, type 'UNKNOWN'"
    )

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
        limit_choices_to=dict(status__in=[NEW, RECRUITING], randomized=False),
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
        grp = " <available>" if not self.patient_group else f" @ {self.patient_group.name}"
        return f"{self.name.title()} ({self.initials.upper()}){grp}"

    def natural_key(self):
        return (self.name,)  # noqa


class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
    verbose_name = "Patient Log"
    verbose_name_plural = "Patient Log"
