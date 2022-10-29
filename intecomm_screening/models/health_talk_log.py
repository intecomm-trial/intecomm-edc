from django.db import models
from edc_model.models import BaseUuidModel
from edc_sites.models import SiteModelMixin

from intecomm_lists.models import HealthFacilities, HealthTalks


class HealthTalkLog(SiteModelMixin, BaseUuidModel):

    hf = models.ForeignKey(
        HealthFacilities, verbose_name="Health facility", on_delete=models.PROTECT
    )

    ht_type = models.ForeignKey(
        HealthTalks, verbose_name="Type of talk", on_delete=models.PROTECT
    )

    report_datetime = models.DateField()

    number_attended = models.IntegerField()

    notes = models.TextField(null=True)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health talk log"
        verbose_name_plural = "Health talk logs"
