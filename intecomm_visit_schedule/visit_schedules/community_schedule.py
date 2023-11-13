from edc_visit_schedule.schedule import Schedule

from ..constants import COMMUNITY_SCHEDULE
from .visits import get_followup_visit, visit00, visit12

community_schedule = Schedule(
    name=COMMUNITY_SCHEDULE,
    verbose_name="Community-based integrated care",
    onschedule_model="intecomm_prn.onschedulecomm",
    offschedule_model="intecomm_prn.offschedulecomm",
    consent_model="intecomm_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)

visits = [visit00]
for month in range(1, 12):
    visits.append(get_followup_visit(month, allow_unscheduled=True))
visits.append(visit12)

for visit in visits:
    community_schedule.add_visit(visit=visit)
