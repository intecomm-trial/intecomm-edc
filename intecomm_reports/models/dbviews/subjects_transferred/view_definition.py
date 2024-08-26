from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    with_stmt = """
        with visits as (
                select subject_identifier, report_datetime, visit_code, visit_code_sequence
                from intecomm_subject_subjectvisit
                group by subject_identifier, report_datetime, visit_code, visit_code_sequence
                order by subject_identifier, report_datetime, visit_code, visit_code_sequence
            )
    """
    sql_view = SqlViewGenerator(
        report_model="intecomm_reports.subjectstransferred_view",
        ordering=["site_id", "subject_identifier"],
        with_stmt=with_stmt,
    )

    subquery = """
        select prn.subject_identifier,
               prn.site_id,
               consent_datetime                                     as consented,
               v.visit_code,
               v.report_datetime                                    as last_visit,
               prn.report_datetime                                  as transferred,
               datediff(prn.report_datetime, consent_datetime) / 30 as months,
               eof.offstudy_datetime                                as offstudy,
               eof.report_datetime                                  as last_seen
        from intecomm_prn_subjecttransfer as prn
            left join edc_registration_registeredsubject as rs on prn.subject_identifier = rs.subject_identifier
            left join intecomm_prn_endofstudy as eof on prn.subject_identifier = eof.subject_identifier
            left join (
                select distinct subject_identifier,
                last_value(report_datetime) OVER w as report_datetime,
                last_value(visit_code) OVER w as visit_code
                from visits WINDOW w as (PARTITION BY `subject_identifier`)
            ) v on prn.subject_identifier = v.subject_identifier
        order by datediff(prn.report_datetime, consent_datetime) / 30 desc, subject_identifier
        """  # noqa

    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
