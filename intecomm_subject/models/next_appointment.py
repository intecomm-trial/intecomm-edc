from __future__ import annotations

from edc_model.models import BaseUuidModel
from edc_next_appointment.model_mixins import NextAppointmentCrfModelMixin

from ..model_mixins import CrfModelMixin


class NextAppointment(NextAppointmentCrfModelMixin, CrfModelMixin, BaseUuidModel):
    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Next Appointment"
        verbose_name_plural = "Next Appointments"
