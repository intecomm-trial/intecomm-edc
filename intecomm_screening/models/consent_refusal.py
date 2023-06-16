from django.db import models
from edc_model.models import BaseUuidModel
from edc_model.models.historical_records import HistoricalRecords
from edc_model_fields.fields.other_charfield import OtherCharField
from edc_search.model_mixins import SearchSlugManager
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow

from intecomm_consent.utils import raise_if_already_consented
from intecomm_lists.models import ConsentRefusalReasons

from ..utils import raise_if_already_refused_consent
from .subject_screening import SubjectScreening


class ConsentRefusalManager(SearchSlugManager, models.Manager):
    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)


class ConsentRefusal(SiteModelMixin, BaseUuidModel):
    subject_screening = models.OneToOneField(SubjectScreening, on_delete=models.PROTECT)

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
        if not self.id:
            raise_if_already_refused_consent(screening_identifier=self.screening_identifier)
        raise_if_already_consented(screening_identifier=self.screening_identifier)
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.screening_identifier} {self.subject_screening.gender} "
            f"{self.subject_screening.age_in_years}"
        )

    def natural_key(self):
        return (self.screening_identifier,)

    def get_search_slug_fields(self):
        return ["screening_identifier"]

    class Meta:
        verbose_name = "Consent Refusal"
        verbose_name_plural = "Consent Refusals"
