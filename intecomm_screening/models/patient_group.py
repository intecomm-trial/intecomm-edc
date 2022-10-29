from django.db import models
from django.db.models import Manager
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from ..choices import GROUP_STATUS_CHOICES
from ..constants import RECRUITING
from .patient_log import PatientLog


class PatientGroup(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    name = models.CharField(
        verbose_name="Group name",
        max_length=25,
        unique=True,
        db_index=True,
    )

    patients = models.ManyToManyField(
        PatientLog,
        # limit_choices_to={"": True, "consented": False},
        blank=True,
    )
    status = models.CharField(
        max_length=25,
        choices=GROUP_STATUS_CHOICES,
        default=RECRUITING,
    )

    randomize = models.CharField(
        verbose_name="Randomise now?", max_length=15, choices=YES_NO, default=NO
    )

    notes = models.TextField(null=True, blank=True)

    on_site = CurrentSiteManager()

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.name.title()

    class Meta(BaseUuidModel.Meta):
        pass
