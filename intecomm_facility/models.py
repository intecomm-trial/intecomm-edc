from django.db import models
from edc_facility.model_mixins import HealthFacilityModelMixin, Manager
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.managers import CurrentSiteManager
from edc_sites.model_mixins import SiteModelMixin


class HealthFacility(SiteModelMixin, HealthFacilityModelMixin, BaseUuidModel):
    distance = models.IntegerField(
        verbose_name="Approximate distance from integrated-care clinic",
        help_text="In km. If within the integrated-care clinic facility type '0'",
    )

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords()

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Facility"
        verbose_name_plural = "Health Facilities"
