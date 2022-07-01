from django.db import models
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.constants import NOT_APPLICABLE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_model import models as edc_models
from edc_reference.model_mixins import ReferenceModelMixin
from edc_sites.models import CurrentSiteManager as BaseCurrentSiteManager
from edc_sites.models import SiteModelMixin
from edc_visit_tracking.managers import VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin

from intecomm_lists.models import ClinicServices, HealthServices

from ..choices import INFO_SOURCE, VISIT_REASON, VISIT_UNSCHEDULED_REASON
from .subject_visit_missed import SubjectVisitMissed


class CurrentSiteManager(VisitModelManager, BaseCurrentSiteManager):
    pass


class SubjectVisit(
    VisitModelMixin,
    ReferenceModelMixin,
    CreatesMetadataModelMixin,
    SiteModelMixin,
    RequiresConsentFieldsModelMixin,
    edc_models.BaseUuidModel,
):
    """A model completed by the user that captures the covering
    information for the data collected for this timepoint/appointment,
    e.g.report_datetime.
    """

    reason = models.CharField(
        verbose_name="What is the reason for this visit report?",
        max_length=25,
        choices=VISIT_REASON,
        help_text=(
            "Only baseline (0m), 6m and 12m are considered "
            "`scheduled` visits as per the INTE protocol."
            f"If `missed' complete CRF {SubjectVisitMissed._meta.verbose_name}."
        ),
    )

    reason_unscheduled = models.CharField(
        verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
        max_length=25,
        choices=VISIT_UNSCHEDULED_REASON,
        default=NOT_APPLICABLE,
    )

    clinic_services = models.ManyToManyField(
        ClinicServices,
        verbose_name="Why is the patient at the clinic today?",
        related_name="visit_clinic_services",
    )

    clinic_services_other = edc_models.OtherCharField()

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

    history = edc_models.HistoricalRecords()

    class Meta(VisitModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
