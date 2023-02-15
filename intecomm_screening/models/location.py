from edc_list_data.model_mixins import ListModelManager, ListModelMixin
from edc_model.models import HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin


class Location(SiteModelMixin, ListModelMixin):
    # TODO:
    # gps data

    # nearest landmark

    # UG #######################

    # street

    # village / city / town

    # parish

    # sub-county

    # county

    # district

    # TZ #######################
    # https://en.wikipedia.org/wiki/Subdivisions_of_Tanzania

    # region (31)

    # district (169 districts )

    # division (contains wards)

    # ward (contains towns and villages) -> village -> hamlet

    # urban_ward (contains parts of or all of a town) -> street

    # village / city / town

    on_site = CurrentSiteManager()
    history = HistoricalRecords()
    objects = ListModelManager()

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
