from django.db import models
from edc_model.models import BaseUuidModel

from intecomm_screening.models import HealthFacility


class IdenfifierFormat(BaseUuidModel):
    health_facility = models.ForeignKey(
        HealthFacility,
        on_delete=models.PROTECT,
    )

    format_name = models.CharField(max_length=50)

    format_regex = models.CharField(max_length=150)

    comment = models.TextField(null=True, blank=True)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Idenfifier format"
        verbose_name_plural = "Idenfifier formats"
