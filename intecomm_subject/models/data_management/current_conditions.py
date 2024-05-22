from django.db import models
from django_pandas.managers import DataFrameManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin


class CurrentConditions(UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):
    """A data management table with details of each participant's
    diagnoses.

    Run `python manage.py update_conditions` to populate.
    """

    baseline_date = models.DateField(null=True)

    hiv = models.BooleanField(default=False)
    htn = models.BooleanField(default=False)
    dm = models.BooleanField(default=False)

    hiv_dx_date = models.DateField(null=True)
    htn_dx_date = models.DateField(null=True)
    dm_dx_date = models.DateField(null=True)

    hiv_dx_days = models.IntegerField(
        default=None, null=True, help_text="Number of days relative to baseline"
    )
    dm_dx_days = models.IntegerField(
        default=None, null=True, help_text="Number of days relative to baseline"
    )
    htn_dx_days = models.IntegerField(
        default=None, null=True, help_text="Number of days relative to baseline"
    )

    comment = models.TextField(null=True)

    objects = DataFrameManager()

    def update_site_on_save(self, *args, **kwargs):
        pass

    class Meta(UniqueSubjectIdentifierFieldMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Current Conditions"
        verbose_name_plural = "Current Conditions"
