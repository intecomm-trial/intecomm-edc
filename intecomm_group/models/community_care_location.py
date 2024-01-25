from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.constants import CLOSED, OPEN
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField
from edc_sites.model_mixins import SiteModelMixin

from intecomm_lists.models import LocationTypes

from ..choices import LOCATION_STATUS


class CommunityCareLocation(SiteModelMixin, BaseUuidModel):
    report_datetime = models.DateTimeField()

    name = models.CharField(max_length=25, unique=True, null=True, blank=False)

    opening_date = models.DateField()

    closing_date = models.DateField(
        null=True,
        blank=True,
        help_text=(
            "Complete the 'closing' date if the location is no longer being used by any group"
        ),
    )

    status = models.CharField(max_length=25, choices=LOCATION_STATUS, default=OPEN)

    location_type = models.ForeignKey(LocationTypes, on_delete=models.PROTECT)

    location_type_other = OtherCharField()

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

    description = models.TextField(null=True, blank=True)

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        self.status = CLOSED if self.opening_date and self.closing_date else OPEN
        if self.gps:
            lat, lon = self.gps.split(",")
            self.latitude = float(lat.strip())
            self.longitude = float(lon.strip())
        super().save(*args, **kwargs)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Community Care Location"
        verbose_name_plural = "Community Care Locations"
