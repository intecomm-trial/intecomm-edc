from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    sql_view = SqlViewGenerator(
        report_model="intecomm_reports.eos_view",
        ordering=["site_id", "subject_identifier"],
    )

    subquery = """
    select subject_identifier, visit_datetime, timepoint, visit_code, visit_code_sequence,
    offstudy_reason, offstudy_datetime, site_id, TIMESTAMPDIFF(MONTH, visit_datetime,
    now()) as m, schedule_status
    from (
        select b1.subject_identifier, max(b1.visit_datetime) as visit_datetime,
        max(b1.timepoint) as timepoint, max(eos.offstudy_datetime) as offstudy_datetime,
        min(baseline_datetime) as baseline_datetime, sched.schedule_status,
        reasons.name as offstudy_reason, appt.visit_code, appt.visit_code_sequence, appt.site_id
		from (
			select v.subject_identifier, max(v.report_datetime) as visit_datetime,
			min(v.report_datetime) as baseline_datetime, max(appt.timepoint) as timepoint
			from intecomm_screening_patientlog as plog
			left join intecomm_subject_subjectvisit as v on v.subject_identifier=plog.subject_identifier
			left join edc_appointment_appointment as appt on v.appointment_id=appt.id
			where plog.group_identifier is not null
			group by v.subject_identifier
        ) as b1
		left join edc_appointment_appointment as appt on (b1.subject_identifier=appt.subject_identifier and b1.timepoint=appt.timepoint)
        left join intecomm_prn_endofstudy as eos on eos.subject_identifier=b1.subject_identifier
        left join intecomm_lists_offstudyreasons as reasons on eos.id=reasons.id
        left join edc_visit_schedule_subjectschedulehistory as sched on b1.subject_identifier=sched.subject_identifier
        group by b1.subject_identifier, sched.schedule_status, reasons.name, appt.visit_code, appt.visit_code_sequence, appt.site_id
        order by b1.subject_identifier
    ) as b2
        """  # noqa

    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
