from uuid import uuid4

from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators import datetime_not_future
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow
from intecomm_form_validators import RECRUITING

from ..choices import GROUP_STATUS_CHOICES


class PatientGroupManager(models.Manager):

    use_in_migrations = True


class PatientGroup(SiteModelMixin, BaseUuidModel):

    group_identifier = models.CharField(max_length=36, null=True)

    group_identifier_as_pk = models.UUIDField(
        max_length=36, default=uuid4, unique=True, editable=False
    )

    report_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_future],
    )

    name = models.CharField(
        verbose_name="Group name",
        max_length=25,
        unique=True,
        db_index=True,
        help_text="The name may be changed at anytime as long as it is unique.",
    )

    patients = models.ManyToManyField(
        "intecomm_screening.PatientLog",
        verbose_name="Patients",
        blank=True,
    )

    hiv_patients = models.ManyToManyField(
        "intecomm_screening.PatientLog",
        verbose_name="HIV-only",
        blank=True,
        related_name="hiv_patients",
        # related_query_name="hiv_patients",
        # through_fields=("patient_group", "hiv_patient"),
    )

    dm_patients = models.ManyToManyField(
        "intecomm_screening.PatientLog",
        verbose_name="DM-only",
        blank=True,
        related_name="dm_patients",
        # related_query_name="dm_patients",
        # through_fields=("patient_group", "dm_patient"),
    )

    htn_patients = models.ManyToManyField(
        "intecomm_screening.PatientLog",
        verbose_name="HTN-only",
        blank=True,
        related_name="htn_patients",
        # related_query_name="htn_patients",
        # through_fields=("patient_group", "htn_patient"),
    )

    multi_patients = models.ManyToManyField(
        "intecomm_screening.PatientLog",
        verbose_name="Multi-morbidity",
        blank=True,
        related_name="multi_patients",
        # related_query_name="multi_patients",
    )

    status = models.CharField(
        max_length=25,
        choices=GROUP_STATUS_CHOICES,
        default=RECRUITING,
    )

    ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True)

    bypass_group_size_min = models.BooleanField(
        verbose_name="Bypass group size minimum of 14",
        default=False,
        help_text="If ticked, you must have consulted with your study coordinator first",
    )

    bypass_group_ratio = models.BooleanField(
        verbose_name="Bypass 2:1 NCD:HIV ratio",
        default=False,
        help_text="If ticked, you must have consulted with your study coordinator first",
    )

    randomize_now = models.CharField(
        verbose_name="Randomize now?", max_length=15, choices=YES_NO, default=NO
    )

    confirm_randomize_now = models.CharField(
        verbose_name="If YES, please confirm by typing the word RANDOMIZE here",
        max_length=15,
        null=True,
        blank=True,
    )

    randomized = models.BooleanField(default=False, blank=True)

    randomized_datetime = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(null=True, blank=True)

    on_site = CurrentSiteManager()

    objects = PatientGroupManager()

    history = HistoricalRecords()

    def __str__(self):
        status = " (R)" if self.randomized else f"<{self.get_status_display()}>"
        return f"{self.name.upper()} {status}" if self.name else f"<new> {self.user_created}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.group_identifier = self.group_identifier_as_pk
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Group"
        verbose_name_plural = "Patient Groups"
