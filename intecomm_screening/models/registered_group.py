from uuid import uuid4

from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager


class RegisteredGroupManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, group_identifier_as_pk):
        return self.get(group_identifier_as_pk=group_identifier_as_pk)


class RegisteredGroup(BaseUuidModel):

    group_identifier = models.CharField(max_length=36, null=True, blank=True, unique=True)

    group_identifier_as_pk = models.CharField(max_length=36, default=uuid4)

    sid = models.CharField(
        verbose_name="SID", max_length=15, null=True, blank=True, unique=True
    )

    registration_datetime = models.DateTimeField(null=True, blank=True)

    randomization_list_model = models.CharField(max_length=150, null=True)

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    objects = RegisteredGroupManager()

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Registered Group"
        verbose_name_plural = "Registered Groups"
        ordering = ["group_identifier"]
