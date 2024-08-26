from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """
        select B1.* from (
        select hivreview.*, dx.baseline_date, TIMESTAMPDIFF(MONTH, baseline_date, vl_date) as m
        from (
        select subject_identifier, crf.site_id, vl as vl_value,
        case when drawn_date is null then cast(crf.report_datetime as DATE) else drawn_date end as vl_date
        from intecomm_subject_hivinitialreview as crf
        left join intecomm_subject_subjectvisit as v on v.id=crf.subject_visit_id
        where vl is not null
        UNION
        select subject_identifier, crf.site_id, vl as vl_value,
        case when drawn_date is null then cast(crf.report_datetime as DATE) else drawn_date end as vl_date
        from intecomm_subject_hivreview as crf
        left join intecomm_subject_subjectvisit as v on v.id=crf.subject_visit_id
        ) as hivreview
        left join intecomm_reports_diagnoses as dx on dx.subject_identifier=hivreview.subject_identifier
        where vl_value is not null) as B1
        """  # noqa

    sql_view = SqlViewGenerator(
        report_model="intecomm_reports.vl_view",
        ordering=["site_id", "subject_identifier"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
