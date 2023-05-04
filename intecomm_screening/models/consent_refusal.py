from django.db import models
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_model.models import BaseUuidModel
from edc_model.models.historical_records import HistoricalRecords
from edc_model_fields.fields.other_charfield import OtherCharField
from edc_search.model_mixins import SearchSlugManager
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from intecomm_lists.models import ConsentRefusalReasons

from .subject_screening import SubjectScreening


class ConsentRefusalManager(SearchSlugManager, models.Manager):
    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class ConsentRefusal(NonUniqueSubjectIdentifierModelMixin, SiteModelMixin, BaseUuidModel):
    subject_screening = models.ForeignKey(SubjectScreening, on_delete=models.PROTECT)

    subject_identifier = models.CharField(max_length=50, editable=False)

    screening_identifier = models.CharField(max_length=50, editable=False)

    report_datetime = models.DateTimeField(
        verbose_name="Report date and time", default=get_utcnow
    )

    reason = models.ForeignKey(
        ConsentRefusalReasons,
        on_delete=models.PROTECT,
        verbose_name="Reason for refusal to consent",
        max_length=25,
        null=True,
        blank=False,
    )

    other_reason = OtherCharField()

    on_site = CurrentSiteManager()
    objects = ConsentRefusalManager()
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.screening_identifier = self.subject_screening.screening_identifier
        self.subject_identifier = self.subject_screening.subject_identifier
        self.subject_identifier_as_pk = self.subject_screening.subject_identifier_as_pk
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.screening_identifier} {self.subject_screening.gender} "
            f"{self.subject_screening.age_in_years}"
        )

    def natural_key(self):
        return (self.subject_identifier,)

    def get_search_slug_fields(self):
        return ["screening_identifier", "subject_identifier"]

    class Meta:
        verbose_name = "Consent Refusal"
        verbose_name_plural = "Consent Refusals"
