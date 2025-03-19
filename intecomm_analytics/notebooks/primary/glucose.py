from datetime import timedelta

import pandas as pd
from edc_model import duration_to_date
from edc_pdutils.dataframes import get_crf

# boudaries for first measurement
default_baseline_lower_bound = -180
default_baseline_upper_bound = 31

# boudaries for last measurement
default_endline_lower_bound = 182

# boundaries for diagnosis
default_days_since_dx = 180

# boundaries for fasting
default_fasting_hours = 8


def dx_duration_to_date(s):
    if pd.isna(s["dx_date"]) & pd.notna(s["dx_ago"]):
        return duration_to_date(s["dx_ago"], s["report_datetime"])
    return s["dx_date"]


def rx_init_duration_to_date(s):
    if pd.isna(s["rx_init_date"]) & pd.notna(s["rx_init_ago"]):
        return duration_to_date(s["rx_init_ago"], s["report_datetime"])
    return s["rx_init_date"]


def get_all_glucose_results(
    df_main: pd.DataFrame, fasting_hours: int = None, days_since_dx: int | None = None
) -> pd.DataFrame:
    """Merge all sources of glucose results for subjects that have a
    DM diagnosis and have fasted for at least 8hrs.
    """
    fasting_hours = fasting_hours or default_fasting_hours
    days_since_dx = days_since_dx or default_days_since_dx
    columns = [
        "subject_identifier",
        "subject_visit_id",
        "visit_code",
        "visit_code_sequence",
        "visit_datetime",
        "reason",
        "reason_unscheduled",
        "reason_unscheduled_other",
        "reason_missed",
        "reason_missed_other",
        "appointment_id",
        "appt_status",
        "appt_timing",
        "site_id",
        "visit_code_str",
        "endline_visit_code",
        "endline_visit_datetime",
        "endline_visit_code_str",
        "glucose_fasting",
        "glucose_fasting_duration_str",
        "glucose_fasting_duration_delta",
        "glucose_date",
        "glucose_value",
        "glucose_quantifier",
        "glucose_units",
        "source",
    ]

    # dminitialreview
    df_dminitialreview = get_crf(
        model="intecomm_subject.dminitialreview",
        subject_visit_model="intecomm_subject.subjectvisit",
    )
    df_dminitialreview["source"] = "intecomm_subject.dminitialreview"

    # CORRECTION: don't filter for visit 1000 because we are using the dx_date
    # later (180 before baseline)
    # df_dminitialreview = df_dminitialreview[(df_dminitialreview.visit_code==1000.0)
    # & (df_dminitialreview.glucose_performed == YES)]

    # dmreview
    # filter followup glucose results to only include for subjects confirmed at baseline
    df_dmreview = get_crf(
        model="intecomm_subject.dmreview", subject_visit_model="intecomm_subject.subjectvisit"
    )
    df_dmreview["source"] = "intecomm_subject.dmreview"
    # CORRECTION: don't filter this by visit, a few baseline glucose values were reported late
    # df_dmreview = df_dmreview[(df_dmreview.visit_code>=1090.0) &
    # (df_dmreview.subject_identifier.isin(df_dminitialreview.subject_identifier))]
    # df_dmreview = df_dmreview[(df_dmreview.subject_identifier.isin(df1.subject_identifier))]
    df_dmreview = df_dmreview[columns].copy()
    df_dmreview.reset_index(drop=True, inplace=True)

    # glucose (CRF)
    df_glucose_crf = get_crf(
        model="intecomm_subject.glucose", subject_visit_model="intecomm_subject.subjectvisit"
    )
    df_glucose_crf["source"] = "intecomm_subject.glucose"
    # CORRECTION: don't filter this by visit, a few baseline glucose values may
    # have been reported late
    # df_glucose_crf = df_glucose_crf[(df_glucose_crf.visit_code>=1090.0)
    # & (df_glucose_crf.subject_identifier.isin(df_dminitialreview.subject_identifier))]
    # df_glucose_crf = df_glucose_crf[(df_glucose_crf.subject_identifier.isin(
    # df1.subject_identifier))]
    df_glucose_crf = df_glucose_crf[columns].copy()
    df_glucose_crf.reset_index(drop=True, inplace=True)

    # bloodresultsglu
    # df_blood_result_glu = get_crf(
    #     model="intecomm_subject.bloodresultsglu",
    #     subject_visit_model="intecomm_subject.subjectvisit",
    # )
    # df_blood_result_glu = df_blood_result_glu[columns].copy()

    # concat all datasets
    df = pd.concat([df_dminitialreview[columns], df_dmreview, df_glucose_crf])
    df.reset_index(drop=True, inplace=True)

    # merge in dx information
    # consolidate dx_date and rx_init_date into single columns
    df_dminitialreview["dm_dx_date"] = df_dminitialreview.apply(dx_duration_to_date, axis=1)
    df_dminitialreview["dm_rx_init_date"] = df_dminitialreview.apply(
        rx_init_duration_to_date, axis=1
    )

    # merge in dx_date and rx_init_date
    df = df.merge(
        df_dminitialreview[["subject_identifier", "dm_dx_date", "dm_rx_init_date"]],
        on="subject_identifier",
        how="left",
    )
    df.reset_index(drop=True, inplace=True)

    # keep only those with a DM diagnosis
    df = df[df.subject_identifier.isin(df_dminitialreview.subject_identifier)].copy()
    df.reset_index(drop=True, inplace=True)

    # only keep fasted for 8hrs or more
    df = df[df.glucose_fasting_duration_delta >= timedelta(hours=fasting_hours)]
    df.reset_index(drop=True, inplace=True)
    # keep those measured less than 180 days before baseline and hiv(-)
    df = df.merge(
        df_main[["subject_identifier", "baseline_datetime", "hiv"]],
        on="subject_identifier",
        how="left",
    )
    df["glucose_date_delta"] = df.glucose_date - df.baseline_datetime
    # df = df[(df.glucose_date_delta >= timedelta(days=-1 * days_since_dx)) & (df.hiv == 0)]
    df.drop(columns=["hiv"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def get_glucose_first(
    df: pd.DataFrame,
    baseline_lower_bound: int = None,
    baseline_upper_bound: int = None,
    path: str | None = None,
) -> pd.DataFrame:
    baseline_lower_bound = baseline_lower_bound or default_baseline_lower_bound
    baseline_upper_bound = baseline_upper_bound or default_baseline_upper_bound
    # df of first measurement
    cond_lower = (df.glucose_date - df.baseline_datetime) >= timedelta(
        days=baseline_lower_bound
    )
    cond_upper = (df.glucose_date - df.baseline_datetime) <= timedelta(
        days=baseline_upper_bound
    )

    df_first = df[cond_lower & cond_upper].copy()

    df_first.sort_values(
        by=["subject_identifier", "glucose_date"], ascending=True, inplace=True
    )
    df_first.reset_index(drop=True, inplace=True)
    df_first = (
        df_first[
            [
                "subject_identifier",
                "baseline_datetime",
                "glucose_date",
                "glucose_value",
                "glucose_units",
                "glucose_fasting_duration_delta",
                "glucose_date_delta",
            ]
        ]
        .groupby(by=["subject_identifier"])
        .agg(["first"])
        .reset_index()
    )

    df_first.columns = ["_".join(col).strip() for col in df_first.columns.values]
    df_first.rename(
        columns={
            "subject_identifier_": "subject_identifier",
            "baseline_datetime_first": "baseline_datetime",
        },
        inplace=True,
    )
    df_first["glucose_fasting_duration_hours_first"] = (
        df_first["glucose_fasting_duration_delta_first"].dt.total_seconds() / 3600
    )
    df_first.reset_index(drop=True, inplace=True)
    if path:
        df_first.to_csv(path / "glucose_df_first.csv", index=False)
    return df_first


def get_glucose_last(
    df: pd.DataFrame, endline_lower_bound: int = None, path: str | None = None
) -> pd.DataFrame:
    """Return a dataframe with the last glucose measurement."""
    endline_lower_bound = endline_lower_bound or default_endline_lower_bound
    df_last = df[
        (df.glucose_date - df.baseline_datetime) >= timedelta(days=endline_lower_bound)
    ].copy()

    df_last.sort_values(
        by=["subject_identifier", "glucose_date"], ascending=True, inplace=True
    )
    df_last.reset_index(drop=True, inplace=True)
    df_last = (
        df_last[
            [
                "subject_identifier",
                "baseline_datetime",
                "glucose_date",
                "glucose_value",
                "glucose_units",
                "glucose_fasting_duration_delta",
                "glucose_date_delta",
            ]
        ]
        .groupby(by=["subject_identifier"])
        .agg(["last"])
        .reset_index()
    )

    df_last.columns = ["_".join(col).strip() for col in df_last.columns.values]
    df_last.rename(
        columns={
            "subject_identifier_": "subject_identifier",
            "baseline_datetime_last": "baseline_datetime",
        },
        inplace=True,
    )
    df_last["glucose_fasting_duration_hours_last"] = (
        df_last["glucose_fasting_duration_delta_last"].dt.total_seconds() / 3600
    )
    df_last.reset_index(drop=True, inplace=True)
    if path:
        df_last.to_csv(path / "glucose_df_last.csv", index=False)
    return df_last


def get_glucose_first_and_last(df: pd.DataFrame, path: str | None = None) -> pd.DataFrame:
    df_first = get_glucose_first(df)
    df_last = get_glucose_last(df)
    df_first_and_last = pd.merge(
        df_first, df_last, on=["subject_identifier", "baseline_datetime"], how="outer"
    )
    df_first_and_last["glucose_measured_days_last"] = (
        df_first_and_last["glucose_date_last"] - df_first_and_last["baseline_datetime"]
    ).dt.days
    df_first_and_last["glucose_measured_days_first"] = (
        df_first_and_last["glucose_date_first"] - df_first_and_last["baseline_datetime"]
    ).dt.days
    df_first_and_last["glucose_first_to_last_days"] = (
        df_first_and_last["glucose_date_last"] - df_first_and_last["glucose_date_first"]
    ).dt.days
    if path:
        df_first_and_last.to_csv(path / "glucose_df_first_and_last.csv", index=False)
    return df_first_and_last
