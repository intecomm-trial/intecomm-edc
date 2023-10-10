from edc_locator.utils import get_locator_model
from edc_visit_schedule.visit_schedule import VisitSchedule

from ..constants import VISIT_SCHEDULE
from .community_schedule import community_schedule
from .facility_schedule import facility_schedule

visit_schedule = VisitSchedule(
    name=VISIT_SCHEDULE,
    verbose_name="INTECOMM",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="intecomm_ae.deathreport",
    locator_model=get_locator_model(),
    previous_visit_schedule=None,
)
visit_schedule.add_schedule(community_schedule)
visit_schedule.add_schedule(facility_schedule)
