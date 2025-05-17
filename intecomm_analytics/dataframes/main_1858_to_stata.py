def to_stata(df_main, path):
    """Export to STATA.

    For example:
        df_main = get_df_main_1858(None)
        to_stata(df_main, my_path)

    Once created, open the DTA in STATA and run the commands from the
    printed output of this func.
    """
    df_main["randomization_list_id"] = df_main["randomization_list_id"].astype(str)
    df_main["vl_baseline"] = df_main["vl_baseline"].astype("Int64")
    df_main["vl_endline"] = df_main["vl_endline"].astype("Int64")
    df_main["vl_baseline_log10"] = df_main["vl_baseline_log10"].astype("Float64")
    df_main["vl_endline_log10"] = df_main["vl_endline_log10"].astype("Float64")
    df_main["primary_vl_endline"] = df_main["primary_vl_endline"].astype("Int64")
    df_main = (
        df_main.rename(
            columns={
                "glucose_fasting_duration_hours_baseline": "glucose_fasting_hours_baseline",
                "primary_vl_controlled_baseline_400": "primary_vl_cntrl_baseline_400",
                "primary_vl_controlled_baseline_50": "primary_vl_cntrl_baseline_50",
                "primary_vl_controlled_endline_400": "primary_vl_cntrl_endline_400",
                "primary_vl_controlled_endline_50": "primary_vl_cntrl_endline_50",
                "glucose_fasting_duration_hours_endline": "glucose_fasting_hours_endline",
            }
        )
        .drop(
            columns=[
                "screening_refusal_reason_other",
                "glucose_fasting_duration_delta_baseline",
                "glucose_fasting_duration_delta_endline",
            ]
        )
        .reset_index(drop=True)
    )

    # convert date to formatted str
    df_main["consent_datetime"] = (
        df_main["consent_datetime"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["allocated_datetime"] = (
        df_main["allocated_datetime"].dt.tz_localize(None).astype("datetime64[ns]")
    )

    df_main["baseline_datetime"] = (
        df_main["baseline_datetime"].dt.tz_localize(None).astype("datetime64[ns]")
    )

    df_main["endline_visit_datetime"] = (
        df_main["endline_visit_datetime"].dt.tz_localize(None).astype("datetime64[ns]")
    )

    df_main["htn_dx_date"] = (
        df_main["htn_dx_date"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["vl_baseline_date"] = (
        df_main["vl_baseline_date"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["dm_dx_date"] = df_main["dm_dx_date"].dt.tz_localize(None).astype("datetime64[ns]")
    df_main["vl_endline_date"] = (
        df_main["vl_endline_date"].dt.tz_localize(None).astype("datetime64[ns]")
    )

    df_main["offstudy_datetime"] = (
        df_main["offstudy_datetime"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["endline_datetime"] = (
        df_main["endline_datetime"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["bp_datetime_first"] = (
        df_main["bp_datetime_first"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["bp_datetime_last"] = (
        df_main["bp_datetime_last"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["glucose_date_baseline"] = (
        df_main["glucose_date_baseline"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["hiv_dx_date"] = (
        df_main["hiv_dx_date"].dt.tz_localize(None).astype("datetime64[ns]")
    )
    df_main["glucose_date_endline"] = (
        df_main["glucose_date_endline"].dt.tz_localize(None).astype("datetime64[ns]")
    )

    # convert timedeltas to seconds
    df_main["hiv_timedelta_dx"] = df_main["hiv_timedelta_dx"].dt.total_seconds()
    df_main["htn_timedelta_dx"] = df_main["htn_timedelta_dx"].dt.total_seconds()
    df_main["dm_timedelta_dx"] = df_main["dm_timedelta_dx"].dt.total_seconds()
    df_main["bp_measured_delta"] = df_main["bp_measured_delta"].dt.total_seconds()
    df_main["glucose_date_delta_baseline"] = df_main[
        "glucose_date_delta_baseline"
    ].dt.total_seconds()
    df_main["glucose_date_delta_endline"] = df_main[
        "glucose_date_delta_endline"
    ].dt.total_seconds()

    df_main.to_stata(
        path=path / "df_main_1858.dta",
        variable_labels=variable_labels(),
        version=118,
        write_index=False,
    )


def variable_labels() -> dict:
    labels = {
        "age_in_years": "age in years",
        "allocated_datetime": "randomization list allocation/assignment datetime",
        "allocation": "randomization list allocation (integer)",
        "assignment": "Intention-to-treat a=comm, b=facility",
        "baseline_datetime": "baseline datetime (first visit date)",
        "bmi": "Body mass index at baseline",
        "bp_controlled_baseline": "BP controlled at baseline",
        "bp_controlled_endline": "BP controlled at endline",
        "bp_datetime_first": "Date for first BP measurement",
        "bp_datetime_last": "Date for last BP measurement",
        "bp_dia_baseline": "Endline diastolic measurement",
        "bp_dia_endline": "Endline diastolic measurement",
        "bp_diastolic_first": "First BP diastolic measurement",
        "bp_diastolic_last": "Last BP diastolic measurement",
        "bp_measured_delta": "seconds between BP baseline/endline measurements",
        "bp_severe_htn_baseline": "Has severe hypertension at baseline",
        "bp_severe_htn_endline": "Has severe hypertension at endline",
        "bp_sys_baseline": "Baseline systolic measurement",
        "bp_sys_endline": "Endline systolic measurement",
        "bp_systolic_first": "First BP systolic measurement",
        "bp_systolic_last": "Last BP systolic measurement",
        "bp_visit_code_first": "Visit code for first BP measurement",
        "bp_visit_code_last": "Visit code for last BP measurement",
        "complication_stroke": "Stroke (See complicationsbaseline)",
        "complication_heart_attack": (
            "Heart attack / heart failure (See complicationsbaseline)"
        ),
        "complication_renal_disease": "Renal (kidney) disease (See complicationsbaseline)",
        "complication_vision": (
            "Vision problems (e.g. blurred vision) (See complicationsbaseline)"
        ),
        "complication_numbness": "Numbness / burning sensation (See complicationsbaseline)",
        "complication_foot_ulcers": "Foot ulcers (See complicationsbaseline)",
        "consent_datetime": "consent datetime",
        "country": "Country",
        "death_date": "Date of death from EoS report",
        "death_cause": "Cause of death from death report",
        "death_date_from_crf": "Date of death from death report",
        "death_days_to_event": "Days to death from baseline",
        "dm": "diabetes confirmed at baseline",
        "dm_dx_date": "Diabetes diagnosis date",
        "dm_only": "Diabetes diagnosis only",
        "dm_scr": "reported diabetes at screening",
        "dm_timedelta_dx": "time since diabetes diagnosis in seconds",
        "dm_years_since_dx": "years since diabetes diagnosis",
        "endline_datetime": "Endline datetime (last visit date)",
        "endline_visit_code": "endline visit code",
        "endline_visit_datetime": "endline datetime",
        "gender": "gender",
        "glucose_controlled_baseline": "Glucose controlled at baseline",
        "glucose_controlled_endline": "Glucose controlled at endline",
        "glucose_date_baseline": "Baseline glucose measurement date",
        "glucose_date_delta_baseline": (
            "Baseline glucose measurement date seconds from true baseline"
        ),
        "glucose_date_delta_endline": (
            "Endline glucose measurement date seconds from true baseline"
        ),
        "glucose_date_endline": "Endline glucose measurement date",
        "glucose_fasting_hours_baseline": "Baseline glucose fasting duration hours ",
        "glucose_fasting_hours_endline": "Endline glucose fasting duration hours ",
        "glucose_first_to_last_days": "Days between first and last glucose measurement",
        "glucose_measured_days_baseline": (
            "Baseline glucose measured in days from true baseline"
        ),
        "glucose_measured_days_endline": "Endline glucose measured in days from true baseline",
        "glucose_resulted_baseline": "1/0 Glucose result available at baseline",
        "glucose_resulted_endline": "1/0 Glucose result available at endline",
        "glucose_units_baseline": "Baseline glucose measurement units",
        "glucose_units_endline": "Endline glucose measurement units",
        "glucose_value_baseline": "Baseline glucose measurement value",
        "glucose_value_endline": "Endline glucose measurement value",
        "group_identifier": "unique group identifier",
        "height": "Height in centimeters",
        "hiv": "HIV confirmed at baseline",
        "hiv_dx_date": "HIV diagnosis date",
        "hiv_only": "HIV only confirmed at baseline",
        "hiv_scr": "reported HIV at screening",
        "hiv_timedelta_dx": "time since HIV diagnosis in seconds",
        "hiv_years_since_dx": "years since HIV diagnosis",
        "htn": "hypertension confirmed at baseline",
        "htn_and_dm": "Hypertension and diabetes confirmed at baseline",
        "hiv_and_htn_and_dm": "HIV and hypertension and diabetes confirmed at baseline",
        "htn_dx_date": "Hypertension diagnosis date",
        "htn_only": "Hypertension diagnosis only",
        "htn_scr": "reported hypertension at screening",
        "htn_timedelta_dx": "time since hypertension diagnosis in seconds",
        "htn_years_since_dx": "years since hypertension diagnosis",
        "ltfu_date": "Date lost to follow up",
        "ncd": "NCD only confirmed at baseline",
        "offstudy_datetime": "Off study datetime",
        "offstudy_reason": "Off study reason",
        "onstudy_days": "Number of days on study",
        "patient_log_identifier": (
            "screening log unique subject/potential participant identifier"
        ),
        "pp": "Per protocol assignment a=comm, b=facility",
        "randomization_list_id": "randomization list id/pk (group)",
        "screening_identifier": "subject screening unique identifier",
        "screening_refusal_reason": "screening refusal reason",
        "screening_refusal_reason_other": "screening refusal reason other",
        "sid": "randomzation list SID (group)",
        "site": "site name",
        "site_id": "site code",
        "stable": "6m stable in care",
        "subject_identifier": "subject/participant unique identifier",
        "transfer_date": "Date transferred",
        "vl_baseline": "Baseline viral load (copies/ml)",
        "vl_baseline_date": "Baseline viral load date",
        "vl_baseline_log10": "Baseline viral load (log10)",
        "vl_controlled_baseline": "VL supressed at baseline <1000",
        "vl_controlled_baseline_400": "VL supressed at baseline <400",
        "vl_controlled_baseline_50": "VL supressed at baseline <50",
        "vl_endline": "Endline viral load (copies/ml)",
        "vl_endline_date": "Endline viral load date",
        "vl_endline_log10": "Endline viral load (log10)",
        "vl_controlled_endline": "VL supressed at endline <1000",
        "vl_controlled_endline_400": "VL supressed at endline <400",
        "vl_controlled_endline_50": "VL supressed at endline <50",
        "willing_to_screen": "willing to screen",
        "primary_cohort": "1=DM_ALONE,2=HTN_ALONE,3=DM+HTN,4=HIV_ALONE,-1=UNDEFINED",
        "endline": "1/0 where 1=Included in endline calculations (See EoS)",
        "primary_cohort_str": "primary_cohort string representation",
        "primary_gl_endline": (
            "Endline glucose for cohort DM_ALONE (1) and DM in cohort HTN_DM (3)"
        ),
        "primary_bp_dia_endline": (
            "Endline BP dia for cohort HTN_ALONE (2) and HTN in cohort HTN_DM (3)"
        ),
        "primary_bp_sys_endline": (
            "Endline BP sys for cohort HTN_ALONE (2) and HTN in cohort HTN_DM (3)"
        ),
        "primary_vl_endline": "Endline VL sys for cohort HIV_ALONE (4)",
        "primary_controlled_endline": (
            "Controlled VL/BP+GL composite at endline. See SAP primary endpoint criteria"
        ),
        "primary_gl_baseline": (
            "Baseline glucose for cohort DM_ALONE (1) and DM in cohort HTN_DM (3)"
        ),
        "primary_gl_controlled_baseline": (
            "1/0 for cohort DM_ALONE (1) and DM in cohort HTN_DM (3)"
        ),
        "primary_gl_cntrl_baseline": "1/0 for cohort DM_ALONE (1) and DM in cohort HTN_DM (3)",
        "primary_bp_sys_baseline": (
            "Baseline BP sys for cohort HTN_ALONE (2) and HTN in cohort HTN_DM (3)"
        ),
        "primary_bp_dia_baseline": (
            "Baseline BP dia for cohort HTN_ALONE (2) and HTN in cohort HTN_DM (3)"
        ),
        "primary_bp_controlled_baseline": (
            "1/0 for cohort HTN_ALONE (2) and HTN in cohort HTN_DM (3)"
        ),
        "primary_vl_baseline": "Baseline VL sys for cohort HIV_ALONE (4)",
        "primary_vl_controlled_baseline": (
            "1/0 for VL<1000 copies/ml at baseline for cohort HIV_ALONE (4)"
        ),
        "primary_vl_controlled_baseline_400": (
            "1/0 for VL<400 copies/ml at baseline for cohort HIV_ALONE (4)"
        ),
        "primary_vl_controlled_baseline_50": (
            "1/0 for VL<50 copies/ml at baseline for cohort HIV_ALONE (4)"
        ),
        "primary_gl_controlled_endline": (
            "1/0 for glucose at baseline for cohort DM_ALONE (1) and DM in cohort HTN_DM (3)"
        ),
        "primary_bp_controlled_endline": (
            "1/0 for BP at baseline for cohort HTN_ALONE (1) and HTN in cohort HTN_DM (3)"
        ),
        "primary_vl_controlled_endline": (
            "1/0 for VL<1000 copies/ml at endline for cohort HIV_ALONE (4)"
        ),
        "primary_vl_controlled_endline_400": (
            "1/0 for VL<400 copies/ml at endline for cohort HIV_ALONE (4)"
        ),
        "primary_vl_controlled_endline_50": (
            "1/0 for VL<50 copies/ml at endline for cohort HIV_ALONE (4)"
        ),
        "primary_vl_cntrl_endline_400": (
            "1/0 for VL<400 copies/ml at endline for cohort HIV_ALONE (4)"
        ),
        "primary_vl_cntrl_endline_50": (
            "1/0 for VL<50 copies/ml at endline for cohort HIV_ALONE (4)"
        ),
        "primary_composite_baseline": (
            "1/0 BP/DM composite at baseline DM_ALONE (1),HTN_ALONE (2),HTN_DM (3)"
        ),
        "primary_composite_endline": (
            "1/0 BP/DM composite at endline DM_ALONE (1),HTN_ALONE (2),HTN_DM (3)"
        ),
        "primary_composite_alt_baseline": (
            "1/0 BP/DM alternative composite at baseline (not in SAP!))"
        ),
        "primary_composite_alt_endline": (
            "1/0 BP/DM alternative composite at endline (not in SAP!))"
        ),
        "employment_status": "Employment status (See otherbaselinedata)",
        "education": (
            "How much formal education does the patient have? (See otherbaselinedata)"
        ),
        "marital_status": "Personal/marital status? (See otherbaselinedata)",
        "smoking_status": "Which of these options describes you? (See otherbaselinedata)",
        "alcohol_consumption": "Do you drink alcohol? How often? (See otherbaselinedata)",
        "weight": "Weight in kg",
    }
    for label, description in labels.items():
        if len(description) > 80:
            raise ValueError(
                "Label description must be 80 characters or fewer. "
                f"Got `{label}` is {len(description)} chars."
            )
    return labels
