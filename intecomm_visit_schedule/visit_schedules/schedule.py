from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule
from edc_visit_schedule import Visit as BaseVisit

from ..constants import DAY1, SCHEDULE
from .crfs import crfs_d1, crfs_missed
from .crfs import crfs_prn as default_crfs_prn
from .crfs import crfs_unscheduled as default_crfs_unscheduled
from .requisitions import requisitions_d1
from .requisitions import requisitions_prn as default_requisitions_prn
from .requisitions import requisitions_unscheduled as default_requisitions_unscheduled


class Visit(BaseVisit):
    def __init__(
        self,
        crfs_unscheduled=None,
        requisitions_unscheduled=None,
        crfs_prn=None,
        requisitions_prn=None,
        allow_unscheduled=None,
        **kwargs,
    ):
        super().__init__(
            allow_unscheduled=True if allow_unscheduled is None else allow_unscheduled,
            crfs_unscheduled=crfs_unscheduled or default_crfs_unscheduled,
            requisitions_unscheduled=requisitions_unscheduled
            or default_requisitions_unscheduled,
            crfs_prn=crfs_prn or default_crfs_prn,
            requisitions_prn=requisitions_prn or default_requisitions_prn,
            crfs_missed=crfs_missed,
            **kwargs,
        )


# schedule for new participants
schedule = Schedule(
    name=SCHEDULE,
    verbose_name="Day 1 to Month 12 Follow-up",
    onschedule_model="intecomm_prn.onschedule",
    offschedule_model="intecomm_prn.offschedule",
    consent_model="intecomm_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)


visit000 = Visit(
    code=DAY1,
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d1,
    crfs=crfs_d1,
    facility_name="7-day-clinic",
)


visits = [
    visit000,
]
for visit in visits:
    schedule.add_visit(visit=visit)
