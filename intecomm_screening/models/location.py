from edc_list_data.model_mixins import ListModelManager, ListModelMixin
from edc_model.models import HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin


class Location(SiteModelMixin, ListModelMixin):
    on_site = CurrentSiteManager()
    history = HistoricalRecords()
    objects = ListModelManager()

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
