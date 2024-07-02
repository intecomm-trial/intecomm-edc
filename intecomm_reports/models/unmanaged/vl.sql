create view intecomm_reports_vl_view as (
    select A.*, dx.baseline_date, TIMESTAMPDIFF(MONTH, baseline_date, vl_date) as m, uuid() as 'id', now() as created, "intecomm_reports.vl" as report_model
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
        ) as A
        left join intecomm_reports_diagnoses as dx on dx.subject_identifier=A.subject_identifier
        where vl_value is not null
        order by subject_identifier, vl_date
)
