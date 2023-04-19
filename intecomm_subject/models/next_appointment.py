from django.db import models
from django.db.models import PROTECT
from edc_model import models as edc_models

from intecomm_screening.models import HealthFacility

from ..choices import APPT_DATE_INFO_SOURCES
from ..constants import INTEGRATED
from ..model_mixins import CrfModelMixin


class NextAppointment(CrfModelMixin, edc_models.BaseUuidModel):
    health_facility = models.ForeignKey(
        HealthFacility,
        on_delete=PROTECT,
        limit_choices_to={"health_facility_type__name": INTEGRATED},
        null=True,
        blank=True,
    )

    appt_date = models.DateField(
        verbose_name="Next scheduled routine/facility appointment",
        null=True,
        blank=False,
        help_text="Should fall on an Integrated clinic day",
    )

    info_source = models.CharField(
        verbose_name="What is the source of this appointment date",
        max_length=15,
        choices=APPT_DATE_INFO_SOURCES,
        null=True,
        blank=False,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Next Appointment"
        verbose_name_plural = "Next Appointments"
