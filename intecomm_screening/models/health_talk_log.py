from django.db import models
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField
from edc_sites.models import SiteModelMixin

from intecomm_lists.models import HealthFacilities, HealthTalks


class HealthTalkLog(SiteModelMixin, BaseUuidModel):
    health_facility_name = models.CharField(max_length=25, null=True, blank=False)

    health_facility = models.ForeignKey(
        HealthFacilities,
        verbose_name="Health facility type",
        on_delete=models.PROTECT,
    )

    health_facility_other = OtherCharField()

    health_talk_type = models.ForeignKey(
        HealthTalks, verbose_name="Type of talk", on_delete=models.PROTECT
    )

    health_talk_type_other = OtherCharField()

    report_date = models.DateField()

    number_attended = models.IntegerField(
        verbose_name="Approximate number attended",
    )

    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.health_facility_name:
            self.health_facility_name = self.health_facility_name.upper()
        super().save(*args, **kwargs)

    class Meta(SiteModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health talk log"
        verbose_name_plural = "Health talk logs"
