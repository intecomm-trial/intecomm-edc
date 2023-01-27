from edc_visit_schedule import Schedule

from ..constants import INTE_SCHEDULE
from .visits import visit00, visit12

inte_schedule = Schedule(
    name=INTE_SCHEDULE,
    verbose_name="facility-based integrated care",
    onschedule_model="intecomm_prn.onscheduleinte",
    offschedule_model="intecomm_prn.offscheduleinte",
    consent_model="intecomm_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)


for visit in [visit00, visit12]:
    inte_schedule.add_visit(visit=visit)
