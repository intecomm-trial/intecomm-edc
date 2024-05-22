from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin


class Vl(UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):
    """A data management table with details of each HIV participant's
    viral load.

    """

    baseline_date = models.DateField(null=True)

    baseline_vl_date = models.DateField(null=True)
    endline_vl_date = models.DateField(null=True)

    min_vl_date = models.DateField(null=True)
    max_vl_date = models.DateField(null=True)

    baseline_vl = models.IntegerField(null=True)
    endline_vl = models.IntegerField(null=True)
