from __future__ import annotations

from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Visit as BaseVisit
from edc_visit_schedule.constants import MONTH0, MONTH12

from .crfs import crfs_d1, crfs_followup, crfs_missed
from .crfs import crfs_prn as default_crfs_prn
from .crfs import crfs_unscheduled as default_crfs_unscheduled
from .requisitions import requisitions_d1, requisitions_followup
from .requisitions import requisitions_prn as default_requisitions_prn
from .requisitions import requisitions_unscheduled as default_requisitions_unscheduled


def get_visit_code(mnth: int):
    if mnth < 10:
        return f"10{mnth*10}"
    return f"1{mnth*10}"


def get_followup_visit(month):
    if month == 0 or month >= 12:
        raise ValueError(f"Invalid month number. Follow visits are from 1-11. Got {month}.")
    rlower = relativedelta(days=13)
    rupper = relativedelta(days=15)
    return Visit(
        code=get_visit_code(month),
        title=f"Followup month {month}",
        timepoint=month,
        rbase=relativedelta(months=month),
        rlower=rlower,
        rupper=rupper,
        add_window_gap_to_lower=True,
        requisitions=requisitions_followup,
        crfs=crfs_followup,
        crfs_unscheduled=crfs_followup,
        facility_name="5-day-clinic",
    )


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


visit00 = Visit(
    code=MONTH0,
    title="Baseline",
    timepoint=0,
    rbase=relativedelta(day=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    add_window_gap_to_lower=True,
    requisitions=requisitions_d1,
    crfs=crfs_d1,
    facility_name="5-day-clinic",
)


visit12 = Visit(
    code=MONTH12,
    title="Month 12 (End of study)",
    timepoint=12,
    rbase=relativedelta(months=12),
    rlower=relativedelta(days=5),
    rupper=relativedelta(days=10),
    add_window_gap_to_lower=True,
    requisitions=requisitions_followup,
    crfs=crfs_followup,
    facility_name="5-day-clinic",
)
