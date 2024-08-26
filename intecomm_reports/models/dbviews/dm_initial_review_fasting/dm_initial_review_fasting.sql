create view dm_initial_review_fasting_view as
    select id as UUID(), 'Diabetes Initial Review' as CRF, subject_identifier, visit_code,
        visit_code_sequence, crf.site_id,
        glucose_fasting_duration_str, glucose_fasting_duration_delta
    from intecomm_subject_dminitialreview as crf
        left join intecomm_subject_subjectvisit as v on v.id=crf.subject_visit_id
    where glucose_fasting="Yes"
      and (glucose_fasting_duration_delta < 28800000000 or glucose_fasting_duration_delta is null)
    order by glucose_fasting_duration_delta
    UNION
    select id as UUID(), 'Diabetes Review' as CRF, subject_identifier, visit_code,
        visit_code_sequence, crf.site_id,
       glucose_fasting_duration_str, glucose_fasting_duration_delta
    from intecomm_subject_dmreview as crf
        left join intecomm_subject_subjectvisit as v on v.id=crf.subject_visit_id
    where glucose_fasting="Yes"
      and (glucose_fasting_duration_delta < 28800000000 or glucose_fasting_duration_delta is null)
    order by glucose_fasting_duration_delta;
