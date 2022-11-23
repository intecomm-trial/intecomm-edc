from django.db import models
from django.db.models import UniqueConstraint
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import formatted_date

from intecomm_lists.models import HealthTalkTypes
from intecomm_screening.models import HealthFacility


class Manager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, health_facility, report_date):
        return self.get(health_facility=health_facility, report_date=report_date)


class HealthTalkLog(SiteModelMixin, BaseUuidModel):

    health_facility = models.ForeignKey(
        HealthFacility,
        verbose_name="Health facility",
        on_delete=models.PROTECT,
    )

    health_talk_type = models.ForeignKey(
        HealthTalkTypes, verbose_name="Type of talk", on_delete=models.PROTECT
    )

    health_talk_type_other = OtherCharField()

    report_date = models.DateField()

    number_attended = models.IntegerField(
        verbose_name="Approximate number attended",
    )

    notes = models.TextField(null=True, blank=True)

    on_site = CurrentSiteManager()
    history = HistoricalRecords()
    objects = Manager()

    def __str__(self):
        dt = formatted_date(self.report_date)
        return f"{self.health_facility} on {dt}"

    def natural_key(self):
        return (
            self.health_facility,
            self.report_date,
        )

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health talk log"
        verbose_name_plural = "Health talk logs"
        constraints = [
            UniqueConstraint(
                "health_facility",
                "report_date",
                name="unique_health_facility_report_date",
                violation_error_message="Only one report expected per facility per day.",
            )
        ]
