from django.db import models
from django.db.models import Manager
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model.validators import datetime_not_future
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from ..choices import GROUP_STATUS_CHOICES
from ..constants import RECRUITING
from .patient_log import PatientLog


class PatientGroup(SiteModelMixin, BaseUuidModel):

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
        PatientLog,
        verbose_name="Membership",
        blank=True,
    )

    status = models.CharField(
        max_length=25,
        choices=GROUP_STATUS_CHOICES,
        default=RECRUITING,
    )

    ratio = models.DecimalField(max_digits=10, decimal_places=4, null=True)

    randomize = models.CharField(
        verbose_name="Randomise now?", max_length=15, choices=YES_NO, default=NO
    )

    randomized = models.BooleanField(default=False, blank=True)

    notes = models.TextField(null=True, blank=True)

    on_site = CurrentSiteManager()

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        status = " (R)" if self.randomized else f"<{self.get_status_display()}>"
        return f"{self.name.upper()} {status}" if self.name else f"<new> {self.user_created}"

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Group"
        verbose_name_plural = "Patient Groups"
