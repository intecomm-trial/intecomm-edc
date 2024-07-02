create view subjects_transferred_view as
(
    select *, uuid() as 'id', now() as created, 'intecomm_reports.subjectstransferred' as report_model
    from (
        with visits as (
            select subject_identifier, report_datetime, visit_code, visit_code_sequence
            from intecomm_subject_subjectvisit
            group by subject_identifier, report_datetime, visit_code, visit_code_sequence
            order by subject_identifier, report_datetime, visit_code, visit_code_sequence
        )
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
    ) as A
);
