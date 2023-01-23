from edc_visit_schedule import VisitSchedule

from ..constants import VISIT_SCHEDULE
from .comm_schedule import comm_schedule
from .inte_schedule import inte_schedule

visit_schedule = VisitSchedule(
    name=VISIT_SCHEDULE,
    verbose_name="INTECOMM",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="intecomm_ae.deathreport",
    locator_model="edc_locator.subjectlocator",
    previous_visit_schedule=None,
)
visit_schedule.add_schedule(comm_schedule)
visit_schedule.add_schedule(inte_schedule)
