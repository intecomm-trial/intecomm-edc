from __future__ import annotations

from dateutil.relativedelta import relativedelta
from edc_visit_schedule.constants import MONTH0, MONTH1, MONTH12
from edc_visit_schedule.visit import Visit

from .crfs import crfs_d1, crfs_followup, crfs_missed, crfs_month12, crfs_prn
from .requisitions import (
    requisitions_d1,
    requisitions_followup,
    requisitions_prn,
    requisitions_unscheduled,
)

visit00 = Visit(
    code=MONTH0,
    title="Baseline",
    add_window_gap_to_lower=False,
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


# facility visit01
visit01 = Visit(
    code=MONTH1,
    title="Followup month 1",
    add_window_gap_to_lower=True,
    allow_unscheduled=True,
    crfs=crfs_followup,
    crfs_missed=crfs_missed,
    crfs_prn=crfs_prn,
    crfs_unscheduled=crfs_followup,
    facility_name="5-day-clinic",
    rbase=relativedelta(months=1),
    requisitions=requisitions_followup,
    requisitions_prn=requisitions_prn,
    requisitions_unscheduled=requisitions_unscheduled,
    rlower=relativedelta(days=28),
    rupper=relativedelta(days=15),
    timepoint=1,
)


visit12 = Visit(
    code=MONTH12,
    title="Month 12 (End of study)",
    add_window_gap_to_lower=True,
    allow_unscheduled=True,
    crfs=crfs_month12,
    crfs_missed=crfs_missed,
    crfs_prn=crfs_prn,
    crfs_unscheduled=crfs_followup,
    facility_name="5-day-clinic",
    rbase=relativedelta(months=12),
    requisitions=requisitions_followup,
    requisitions_prn=requisitions_prn,
    requisitions_unscheduled=requisitions_unscheduled,
    rlower=relativedelta(days=13),
    rupper=relativedelta(months=6),
    timepoint=12,
)


def get_visit_code(mnth: int):
    if mnth < 10:
        return f"10{mnth*10}"
    return f"1{mnth*10}"


def get_followup_visit(month, start: int | None = None, allow_unscheduled: bool | None = None):
    start = 0 if start is None else start
    allow_unscheduled = False if allow_unscheduled is None else allow_unscheduled
    if month == start or month >= 12:
        raise ValueError(
            f"Invalid month number. Follow visits are from {start}-11. Got {month}."
        )
    rlower = relativedelta(days=13)
    rupper = relativedelta(days=15)
    return Visit(
        code=get_visit_code(month),
        title=f"Followup month {month}",
        add_window_gap_to_lower=True,
        allow_unscheduled=allow_unscheduled,
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
