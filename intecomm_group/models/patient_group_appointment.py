from django.db import models
from edc_appointment.constants import NEW_APPT
from edc_model.models import BaseUuidModel
from edc_utils import get_utcnow

from ..choices import APPT_STATUS
from .community_care_location import CommunityCareLocation
from .patient_group import PatientGroup


class PatientGroupAppointment(BaseUuidModel):
    report_datetime = models.DateTimeField(default=get_utcnow)

    patient_group = models.ForeignKey(
        PatientGroup,
        on_delete=models.PROTECT,
        blank=False,
    )

    community_care_location = models.ForeignKey(
        CommunityCareLocation,
        on_delete=models.PROTECT,
        blank=False,
    )

    appt_datetime = models.DateTimeField()

    appt_status = models.CharField(max_length=25, choices=APPT_STATUS, default=NEW_APPT)

    notes = models.TextField(null=True, blank=True)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Group Appointment"
        verbose_name_plural = "Patient Group Appointments"
