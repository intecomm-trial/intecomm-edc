from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_model_fields.fields import OtherCharField

from intecomm_lists.models import ClinicServices, HealthServices

from ..model_mixins import CrfModelMixin


class ReasonForVisit(CrfModelMixin, BaseUuidModel):

    health_services = models.ManyToManyField(
        HealthServices,
        related_name="health_services",
        verbose_name="Which health service(s) is the patient here for today?",
    )

    clinic_services = models.ManyToManyField(
        ClinicServices,
        related_name="clinic_services",
        verbose_name="Why is the patient at the clinic?",
    )

    clinic_services_other = OtherCharField()

    refill_hiv = models.CharField(
        verbose_name="Is the patient refilling HIV medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    refill_dm = models.CharField(
        verbose_name="Is the patient refilling Diabetes medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    refill_htn = models.CharField(
        verbose_name="Is the patient refilling Hypertension medications?",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Reason for Visit"
        verbose_name_plural = "Reason for Visits"
