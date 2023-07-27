from django.db import models
from edc_model.models import BaseUuidModel

from intecomm_facility.models import HealthFacility


# TODO: not used, Remove after migrations are squashed/reset
class IdentifierFormat(BaseUuidModel):
    old_health_facility = models.CharField(max_length=100, null=True)

    health_facility = models.ForeignKey(
        HealthFacility,
        verbose_name="Health facility",
        on_delete=models.PROTECT,
        null=True,
    )

    format_name = models.CharField(max_length=50)

    format_regex = models.CharField(max_length=150)

    comment = models.TextField(null=True, blank=True)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Idenfifier format"
        verbose_name_plural = "Idenfifier formats"
