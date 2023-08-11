from __future__ import annotations

from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Visit
from edc_visit_schedule.constants import MONTH0, MONTH12

from .crfs import crfs_d1, crfs_followup, crfs_missed, crfs_prn
from .requisitions import (
    requisitions_d1,
    requisitions_followup,
    requisitions_prn,
    requisitions_unscheduled,
)

visit00 = Visit(
    code=MONTH0,
    title="Baseline",
    add_window_gap_to_lower=True,
    allow_unscheduled=True,
    crfs=crfs_d1,
    crfs_missed=crfs_missed,
    crfs_prn=crfs_prn,
    crfs_unscheduled=crfs_followup,
    facility_name="5-day-clinic",
    rbase=relativedelta(day=0),
    requisitions=requisitions_d1,
    requisitions_prn=requisitions_prn,
    requisitions_unscheduled=requisitions_unscheduled,
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    timepoint=0,
)


visit12 = Visit(
    code=MONTH12,
    title="Month 12 (End of study)",
    add_window_gap_to_lower=True,
    allow_unscheduled=False,
    crfs=crfs_followup,
    crfs_missed=crfs_missed,
    crfs_prn=crfs_prn,
    crfs_unscheduled=crfs_followup,
    facility_name="5-day-clinic",
    rbase=relativedelta(months=12),
    requisitions=requisitions_followup,
    requisitions_prn=requisitions_prn,
    requisitions_unscheduled=requisitions_unscheduled,
    rlower=relativedelta(days=5),
    rupper=relativedelta(days=10),
    timepoint=12,
)


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
        add_window_gap_to_lower=True,
        allow_unscheduled=False,
        crfs=crfs_followup,
        crfs_missed=crfs_missed,
        crfs_prn=crfs_prn,
        crfs_unscheduled=crfs_followup,
        facility_name="5-day-clinic",
        rbase=relativedelta(months=month),
        requisitions=requisitions_followup,
        requisitions_prn=requisitions_prn,
        requisitions_unscheduled=requisitions_unscheduled,
        rlower=rlower,
        rupper=rupper,
        timepoint=month,
    )
