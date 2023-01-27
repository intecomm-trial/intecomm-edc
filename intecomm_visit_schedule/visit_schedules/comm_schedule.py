from edc_visit_schedule import Schedule

from ..constants import COMM_SCHEDULE
from .visits import (
    visit00,
    visit01,
    visit02,
    visit03,
    visit04,
    visit05,
    visit06,
    visit07,
    visit08,
    visit09,
    visit10,
    visit11,
    visit12,
)

comm_schedule = Schedule(
    name=COMM_SCHEDULE,
    verbose_name="community-based integrated care",
    onschedule_model="intecomm_prn.onschedulecomm",
    offschedule_model="intecomm_prn.offschedulecomm",
    consent_model="intecomm_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)


for visit in [
    visit00,
    visit01,
    visit02,
    visit03,
    visit04,
    visit05,
    visit06,
    visit07,
    visit08,
    visit09,
    visit10,
    visit11,
    visit12,
]:
    comm_schedule.add_visit(visit=visit)
