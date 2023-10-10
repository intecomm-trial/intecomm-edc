from edc_visit_schedule.schedule import Schedule

from ..constants import FACILITY_SCHEDULE
from .visits import get_followup_visit, visit00, visit01, visit12

facility_schedule = Schedule(
    name=FACILITY_SCHEDULE,
    verbose_name="Facility-based integrated care",
    onschedule_model="intecomm_prn.onscheduleinte",
    offschedule_model="intecomm_prn.offscheduleinte",
    consent_model="intecomm_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)

visits = [visit00, visit01]
for month in range(2, 12):
    visits.append(get_followup_visit(month, start=1, allow_unscheduled=True))
visits.append(visit12)

for visit in visits:
    facility_schedule.add_visit(visit=visit)
