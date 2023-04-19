from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from intecomm_lists.models import HealthFacilityTypes


class Manager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class HealthFacility(SiteModelMixin, BaseUuidModel):
    report_datetime = models.DateTimeField(default=get_utcnow)

    name = models.CharField(max_length=25, unique=True)

    health_facility_type = models.ForeignKey(
        HealthFacilityTypes,
        verbose_name="Health facility type",
        on_delete=models.PROTECT,
    )

    health_facility_type_other = OtherCharField()

    distance = models.IntegerField(
        verbose_name="Approximate distance from integrated-care clinic",
        help_text="In km. If within the integrated-care clinic facility type '0'",
    )

    gps = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="copy and paste directly from google maps",
    )

    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True,
        help_text="in degrees. copy and paste directly from google maps",
    )

    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True,
        help_text="in degrees. copy and paste directly from google maps",
    )

    mon = models.BooleanField()
    tue = models.BooleanField()
    wed = models.BooleanField()
    thu = models.BooleanField()
    fri = models.BooleanField()
    sat = models.BooleanField()

    notes = models.TextField(null=True, blank=True)

    on_site = CurrentSiteManager()
    history = HistoricalRecords()
    objects = Manager()

    def __str__(self):
        return f"{self.name} {self.health_facility_type.display_name}"

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.name,)

    @property
    def clinic_days(self) -> list[int]:
        """Using ISO numbering where Monday=1."""
        days = []
        if self.mon:
            days.append(1)
        if self.tue:
            days.append(2)
        if self.wed:
            days.append(3)
        if self.thu:
            days.append(4)
        if self.fri:
            days.append(5)
        if self.sat:
            days.append(6)
        return days

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Facility"
        verbose_name_plural = "Health Facilities"
