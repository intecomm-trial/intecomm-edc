from django.db import models
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED

from ..choices import MEETING_STATUS
from ..constants import ATTENDED
from .patient_group_appointment import PatientGroupAppointment


class PatientGroupMeeting(SiteModelMixin, BaseUuidModel):
    patient_group_appointment = models.OneToOneField(
        PatientGroupAppointment,
        on_delete=models.PROTECT,
        blank=False,
    )

    status = models.CharField(max_length=25, choices=MEETING_STATUS, default=SCHEDULED)

    report_datetime = models.DateTimeField(default=get_utcnow)

    meeting_datetime = models.DateTimeField(null=True, blank=True)

    patients = models.ManyToManyField("intecomm_screening.PatientLog", verbose_name="Patients")

    notes = models.TextField(null=True, blank=True)

    # duration,

    def __str__(self):
        return self.patient_group_appointment.patient_group.name

    def save(self, *args, **kwargs):
        self.status = ATTENDED if self.meeting_datetime else SCHEDULED
        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Patient Group Meeting"
        verbose_name_plural = "Patient Groups Meeting"
