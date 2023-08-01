from __future__ import annotations

from django.db import models
from edc_model.models import BaseUuidModel
from edc_next_appointment.choices import APPT_DATE_INFO_SOURCES
from edc_next_appointment.model_mixins import NextAppointmentCrfModelMixin

from ..model_mixins import CrfModelMixin


class NextAppointment(NextAppointmentCrfModelMixin, CrfModelMixin, BaseUuidModel):
    # TODO: Remove field after migrations are squashed/reset
    old_health_facility = models.CharField(
        max_length=100,
        null=True,
    )

    # TODO: Remove field after migrations are squashed/reset
    info_source_old = models.CharField(
        verbose_name="What is the source of this appointment date",
        max_length=15,
        choices=APPT_DATE_INFO_SOURCES,
        null=True,
        blank=False,
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Next Appointment"
        verbose_name_plural = "Next Appointments"
