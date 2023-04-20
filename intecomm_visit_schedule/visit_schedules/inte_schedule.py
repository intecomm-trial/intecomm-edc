from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Crf, FormsCollection, Schedule
from edc_visit_schedule.constants import MONTH0

from ..constants import INTE_SCHEDULE
from .requisitions import requisitions_d1
from .visits import Visit, visit12


def get_visit_code(mnth: int):
    if mnth < 10:
        return f"10{mnth*10}"
    return f"1{mnth*10}"


inte_schedule = Schedule(
    name=INTE_SCHEDULE,
    verbose_name="facility-based integrated care",
    onschedule_model="intecomm_prn.onscheduleinte",
    offschedule_model="intecomm_prn.offscheduleinte",
    consent_model="intecomm_consent.subjectconsent",
    appointment_model="edc_appointment.appointment",
)

crfs_d1 = FormsCollection(
    Crf(show_order=100, model="intecomm_subject.clinicalreviewbaseline"),
    Crf(show_order=110, model="intecomm_subject.vitals"),
    Crf(show_order=120, model="intecomm_subject.hivinitialreview", required=False),
    Crf(show_order=130, model="intecomm_subject.dminitialreview", required=False),
    Crf(show_order=140, model="intecomm_subject.htninitialreview", required=False),
    Crf(show_order=143, model="intecomm_subject.medications"),
    Crf(show_order=145, model="intecomm_subject.drugrefillhtn", required=False),
    Crf(show_order=150, model="intecomm_subject.drugrefilldm", required=False),
    Crf(show_order=155, model="intecomm_subject.drugrefillhiv", required=False),
    Crf(show_order=160, model="intecomm_subject.otherbaselinedata"),
    Crf(show_order=165, model="intecomm_subject.complicationsbaseline"),
    Crf(show_order=175, model="intecomm_subject.nextappointment"),
    name="day1",
)

crfs_followup = FormsCollection(
    Crf(show_order=100, model="intecomm_subject.clinicalreview"),
    Crf(show_order=110, model="intecomm_subject.vitals"),
    Crf(show_order=120, model="intecomm_subject.hivinitialreview", required=False),
    Crf(show_order=130, model="intecomm_subject.dminitialreview", required=False),
    Crf(show_order=140, model="intecomm_subject.htninitialreview", required=False),
    Crf(show_order=143, model="intecomm_subject.medications"),
    Crf(show_order=145, model="intecomm_subject.drugrefillhtn", required=False),
    Crf(show_order=150, model="intecomm_subject.drugrefilldm", required=False),
    Crf(show_order=155, model="intecomm_subject.drugrefillhiv", required=False),
    Crf(show_order=165, model="intecomm_subject.complicationsfollowup"),
    Crf(show_order=175, model="intecomm_subject.healtheconomics"),
    Crf(show_order=185, model="intecomm_subject.nextappointment"),
    name="day1",
)

visit00 = Visit(
    code=MONTH0,
    title="Baseline",
    timepoint=0,
    rbase=relativedelta(day=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d1,
    crfs=crfs_d1,
    crfs_unscheduled=crfs_followup,
    facility_name="5-day-clinic",
)
visits = [visit00]
for month in range(1, 12):
    visits.append(
        Visit(
            code=get_visit_code(month),
            title=f"Followup month {month}",
            timepoint=month,
            rbase=relativedelta(months=month),
            rlower=relativedelta(days=14),
            rupper=relativedelta(days=15),
            requisitions=requisitions_d1,
            crfs=crfs_followup,
            # crfs_unscheduled=crfs_followup,
            facility_name="5-day-clinic",
        )
    )
visits.append(visit12)

for visit in visits:
    inte_schedule.add_visit(visit=visit)
