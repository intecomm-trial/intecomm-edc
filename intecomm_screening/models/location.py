from edc_list_data.model_mixins import ListModelMixin


class Location(ListModelMixin):
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
