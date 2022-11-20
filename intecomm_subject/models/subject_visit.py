from django.db import models
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_offstudy.model_mixins import OffstudyNonCrfModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_sites.models import CurrentSiteManager as BaseCurrentSiteManager
from edc_sites.models import SiteModelMixin
from edc_visit_tracking.managers import VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin

from intecomm_lists.models import ClinicServices, HealthServices

from ..choices import INFO_SOURCE, VISIT_REASON, VISIT_UNSCHEDULED_REASON


class CurrentSiteManager(VisitModelManager, BaseCurrentSiteManager):
    pass


class SubjectVisit(
    VisitModelMixin,
    ReferenceModelMixin,
    CreatesMetadataModelMixin,
    SiteModelMixin,
    RequiresConsentFieldsModelMixin,
    OffstudyNonCrfModelMixin,
    BaseUuidModel,
):
    """A model completed by the user that captures the covering
    information for the data collected for this timepoint/appointment,
    e.g.report_datetime.
    """

    reason = models.CharField(
        verbose_name="What is the reason for this visit report?",
        max_length=25,
        choices=VISIT_REASON,
        help_text="If 'missed', fill in the separate missed visit report",
    )

    reason_unscheduled = models.CharField(
        verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
        max_length=25,
        choices=VISIT_UNSCHEDULED_REASON,
        default=NOT_APPLICABLE,
    )

    unschedule_self_referral = models.CharField(
        verbose_name="If 'unschedule', is this a self-referral?",
        max_length=25,
        choices=YES_NO,
        default=NO,
    )

    unschedule_detail = models.TextField(
        verbose_name="If 'unschedule', please provide further details, if any",
        null=True,
        blank=True,
    )

    clinic_services = models.ManyToManyField(
        ClinicServices,
        verbose_name="Why is the patient at the clinic today?",
        related_name="visit_clinic_services",
    )

    clinic_services_other = OtherCharField()

    health_services = models.ManyToManyField(
        HealthServices,
        verbose_name="Which health service(s) is the patient here for today?",
        related_name="visit_health_services",
    )

    info_source = models.CharField(
        verbose_name="What is the main source of this information?",
        max_length=25,
        choices=INFO_SOURCE,
    )

    on_site = CurrentSiteManager()

    objects = VisitModelManager()

    history = HistoricalRecords()

    class Meta(VisitModelMixin.Meta, BaseUuidModel.Meta):
        pass
