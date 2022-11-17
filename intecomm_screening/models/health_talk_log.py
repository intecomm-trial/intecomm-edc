from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_sites.models import CurrentSiteManager, SiteModelMixin

from intecomm_lists.models import HealthFacilityTypes, HealthTalkTypes
from intecomm_screening.models import HealthFacility


class Manager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, health_facility_name, report_date):
        return self.get(health_facility_name=health_facility_name, report_date=report_date)


class HealthTalkLog(SiteModelMixin, BaseUuidModel):

    health_facility = models.ForeignKey(
        HealthFacility,
        verbose_name="Health facility",
        on_delete=models.PROTECT,
    )

    health_facility_type = models.ForeignKey(
        HealthFacilityTypes,
        verbose_name="Health facility type",
        on_delete=models.PROTECT,
    )

    health_facility_type_other = OtherCharField()

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

    def save(self, *args, **kwargs):
        if self.health_facility_name:
            self.health_facility_name = self.health_facility_name.upper()
        super().save(*args, **kwargs)

    def natural_key(self):
        return (
            self.health_facility_name,
            self.report_date,
        )

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health talk log"
        verbose_name_plural = "Health talk logs"
        constraints = [
            UniqueConstraint(
                Lower("health_facility").desc(),
                name="unique_lower_name_report_date",
            )
        ]
