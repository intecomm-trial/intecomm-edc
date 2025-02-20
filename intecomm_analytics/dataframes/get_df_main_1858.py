from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from edc_constants.constants import NO, OTHER, YES
from edc_model import duration_to_date
from edc_model_to_dataframe import read_frame_edc
from edc_pdutils.dataframes import get_crf, get_subject_visit
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.models import RandomizationList

from intecomm_prn.models import EndOfStudy

from .get_patientlog_df import get_patientlog_df
from .get_vl_summary import VlSummary2

__all__ = ["get_df_main_1858", "treatment_arm_labels"]

from ..notebooks.primary.glucose import (
    get_all_glucose_results,
    get_glucose_first,
    get_glucose_last,
)

treatment_arm_labels = {COMMUNITY_ARM: "Community", FACILITY_ARM: "Facility"}


def glucose_controlled(value):
    if value < 7.00:
        return YES
    elif value >= 7.00:
        return NO
    return "Missing"


def get_ncd(s):
    if (s["htn"] == 1 or s["dm"] == 1) and s["hiv"] == 0:
        return 1
    return 0


def get_hiv_only(s):
    if s["htn"] == 0 and s["dm"] == 0 and s["hiv"] == 1:
        return 1
    return 0


def get_htn_only(s):
    if s["htn"] == 1 and s["dm"] == 0 and s["hiv"] == 0:
        return 1
    return 0


def get_dm_only(s):
    if s["htn"] == 0 and s["dm"] == 1 and s["hiv"] == 0:
        return 1
    return 0


def get_dx_date(s):
    if pd.isna(s["dx_date"]) and not pd.isna(s["dx_ago"]):
        dx_calculated_date = duration_to_date(s["dx_ago"], s["visit_datetime"])
        return dx_calculated_date
    return s["dx_date"]


def get_country(s):
    if s["site_id"] < 200:
        return "UG"
    elif s["site_id"] >= 200:
        return "TZ"
    return "ERROR"


def get_df_main_1858(export_folder: Path | None) -> pd.DataFrame:
    """Trial population"""
    # export_folder = export_folder or Path(
    #     "/Users/erikvw/Documents/ucl/protocols/intecomm/analysis/primary/"
    # )

    # df_screen = read_frame(SubjectScreening.objects.all())
    # df_screen[df_screen.eligible == 1].count()
    # conditions at grouping

    # start with patient log
    df_main = get_patientlog_df()

    # exlude thos not in a group
    df_main = df_main[(df_main.group_identifier.notna())]

    # rename conditions to distinguis as reported at screen
    df_main.rename(columns={"hiv": "hiv_scr", "htn": "htn_scr", "dm": "dm_scr"}, inplace=True)

    # merge with df_visit
    df_main = merge_in_visit(df_main)

    # 1858 subjects

    df_main = merge_in_rando(df_main)

    df_main = merge_in_baseline_conditions(df_main)

    # create ncd column and hiv_only column
    df_main["ncd"] = df_main.apply(get_ncd, axis=1)
    df_main["hiv_only"] = df_main.apply(get_hiv_only, axis=1)
    df_main["htn_only"] = df_main.apply(get_htn_only, axis=1)
    df_main["dm_only"] = df_main.apply(get_dm_only, axis=1)

    df_main = merge_in_vl(df_main)

    df_main = merge_in_eos(df_main)

    df_main["onstudy_days"] = (df_main.endline_datetime - df_main.baseline_datetime).dt.days

    df_main = merge_in_bp(df_main)

    df_main = merge_in_glucose(df_main)

    df_main["country"] = df_main.apply(get_country, axis=1)

    if export_folder:
        df_main.to_csv(
            Path(export_folder) / "df_main_1858.csv",
            index=False,
        )
    return df_main


def validate_df_main(df: pd.DataFrame):

    assert df[df.hiv_only == 1].hiv_only.count() == 526  # nosec B101
    assert df[df.ncd == 1].ncd.count() == 1223  # nosec B101
    assert len(df[(df.hiv_only == 0) & (df.ncd == 0)]) == 109  # nosec B101
    assert list(df.columns) == [  # nosec B101
        "subject_identifier",
        "site",
        "gender",
        "age_in_years",
        "patient_log_identifier",
        "screening_identifier",
        "group_identifier",
        "stable",
        "willing_to_screen",
        "screening_refusal_reason",
        "screening_refusal_reason_other",
        "consent_datetime",
        "site_id",
        "dm",
        "hiv",
        "htn",
        "ncd",
        "hiv_only",
        "assignment",
        "hiv_years_since_dx",
        "hiv_timedelta_dx",
        "htn_years_since_dx",
        "htn_timedelta_dx",
        "dm_years_since_dx",
        "dm_timedelta_dx",
    ]
    print("ok!")


def get_offstudy_reason(s):
    if s["offstudy_reason_name"] == OTHER:
        return s["other_offstudy_reason"]
    return s["offstudy_reason_name"]


def merge_in_visit(df_main: pd.DataFrame) -> pd.DataFrame:
    """Merge in visit.

    Assume if visit 1000 exists => patient is on trial.

    Remove 107-208-0014-2 (incorrectly registered)
    """

    df_visit = get_subject_visit("intecomm_subject.subjectvisit")
    df_visit = df_visit[
        (df_visit.visit_code == 1000.0) & ~(df_visit.subject_identifier == "107-208-0014-2")
    ]
    df_main = pd.merge(
        df_visit[
            [
                "subject_identifier",
                "baseline_datetime",
                "endline_visit_datetime",
                "endline_visit_code",
            ]
        ],
        df_main,
        on="subject_identifier",
        how="left",
    )
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_rando(df_main: pd.DataFrame) -> pd.DataFrame:
    """Add assignment, etc from merge with RandomizationList.

    Note: unit of randomization is the group, not the subject."""
    df_rando = read_frame(
        RandomizationList.objects.values(
            "id",
            "sid",
            "group_identifier",
            "assignment",
            "allocation",
            "allocated_datetime",
        ).filter(group_identifier__isnull=False)
    )
    df_rando = df_rando[df_rando.group_identifier.notna()]
    df_rando.rename(columns={"id": "randomization_list_id"}, inplace=True)
    df_rando.reset_index(drop=True, inplace=True)
    df_main = df_main.merge(
        df_rando[
            [
                "randomization_list_id",
                "group_identifier",
                "sid",
                "assignment",
                "allocation",
                "allocated_datetime",
            ]
        ],
        on="group_identifier",
        how="left",
    )
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_eos(df_main: pd.DataFrame) -> pd.DataFrame:
    """Merge in eos / offstudy"""
    df_eos = read_frame_edc(EndOfStudy.objects.all(), read_frame_verbose=False)
    df_eos["offstudy_reason"] = df_eos.apply(get_offstudy_reason, axis=1)
    df_eos.drop(columns=["offstudy_reason_name"], inplace=True)
    df_eos["endline_datetime"] = df_eos["offstudy_datetime"]
    df_main = df_main.merge(
        df_eos[
            [
                "subject_identifier",
                "offstudy_datetime",
                "offstudy_reason",
                "endline_datetime",
                "ltfu_date",
                "death_date",
                "transfer_date",
            ]
        ],
        on="subject_identifier",
        how="left",
    )
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_vl(df_main: pd.DataFrame) -> pd.DataFrame:
    vl = VlSummary2(
        offset_by="days", baseline_upper=61, endline_upper=182, skip_update_dx=True
    )
    df_vl = vl.to_dataframe()
    df_main = df_main.merge(
        df_vl[
            [
                "subject_identifier",
                "baseline_vl",
                "baseline_vl_date",
                "endline_vl",
                "endline_vl_date",
            ]
        ],
        on="subject_identifier",
        how="left",
    )
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_baseline_conditions(df_main: pd.DataFrame) -> pd.DataFrame:
    """Conditions from the baseline initial forms with dx
    duration.
    """

    subject_identifiers = list(df_main.subject_identifier.unique())
    opts = dict(
        subject_visit_model="intecomm_subject.subjectvisit",
        subject_identifiers=subject_identifiers,
    )
    df_hiv_initial = get_crf(model="intecomm_subject.hivinitialreview", **opts)
    df_htn_initial = get_crf(model="intecomm_subject.htninitialreview", **opts)
    df_dm_initial = get_crf(model="intecomm_subject.dminitialreview", **opts)

    # recalculate dx_date if from dx_ago
    df_hiv_initial["hiv_dx_date"] = df_hiv_initial.apply(get_dx_date, axis=1)
    df_htn_initial["htn_dx_date"] = df_htn_initial.apply(get_dx_date, axis=1)
    df_dm_initial["dm_dx_date"] = df_dm_initial.apply(get_dx_date, axis=1)

    df_hiv_initial["hiv_timedelta_dx"] = pd.to_datetime(
        df_hiv_initial["visit_datetime"]
    ) - pd.to_datetime(df_hiv_initial["hiv_dx_date"])
    df_htn_initial["htn_timedelta_dx"] = pd.to_datetime(
        df_htn_initial["visit_datetime"]
    ) - pd.to_datetime(df_htn_initial["htn_dx_date"])
    df_dm_initial["dm_timedelta_dx"] = pd.to_datetime(
        df_dm_initial["visit_datetime"]
    ) - pd.to_datetime(df_dm_initial["dm_dx_date"])

    df_hiv_initial["hiv_years_since_dx"] = df_hiv_initial["hiv_timedelta_dx"].dt.days / 365
    df_hiv_initial["hiv"] = 1
    df_htn_initial["htn_years_since_dx"] = df_htn_initial["htn_timedelta_dx"].dt.days / 365
    df_htn_initial["htn"] = 1
    df_dm_initial["dm_years_since_dx"] = df_dm_initial["dm_timedelta_dx"].dt.days / 365
    df_dm_initial["dm"] = 1

    df_delta = pd.merge(
        df_hiv_initial[
            [
                "subject_identifier",
                "hiv",
                "hiv_dx_date",
                "hiv_years_since_dx",
                "hiv_timedelta_dx",
            ]
        ],
        df_htn_initial[
            [
                "subject_identifier",
                "htn",
                "htn_dx_date",
                "htn_years_since_dx",
                "htn_timedelta_dx",
            ]
        ],
        on="subject_identifier",
        how="outer",
    )
    df_delta = df_delta.merge(
        df_dm_initial[
            [
                "subject_identifier",
                "dm",
                "dm_dx_date",
                "dm_years_since_dx",
                "dm_timedelta_dx",
            ]
        ],
        on="subject_identifier",
        how="outer",
    )

    df_delta["hiv"] = df_delta["hiv"].fillna(0.0)
    df_delta["htn"] = df_delta["htn"].fillna(0.0)
    df_delta["dm"] = df_delta["dm"].fillna(0.0)
    df_main = df_main.merge(df_delta, on="subject_identifier", how="left")
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def get_diastolic(s):
    if pd.notna(get_systolic(s)):
        if pd.notna(s["dia_blood_pressure_one"]) and pd.notna(s["dia_blood_pressure_two"]):
            return s["dia_blood_pressure_avg"]
        elif pd.notna(s["dia_blood_pressure_one"]) and pd.isna(s["dia_blood_pressure_two"]):
            return s["dia_blood_pressure_one"]
    return np.nan


def get_systolic(s):
    if pd.notna(s["sys_blood_pressure_one"]) and pd.notna(s["sys_blood_pressure_two"]):
        return s["sys_blood_pressure_avg"]
    elif pd.notna(s["sys_blood_pressure_one"]) and pd.isna(s["sys_blood_pressure_two"]):
        return s["sys_blood_pressure_one"]
    return np.nan


def get_bp_measured(s):
    if pd.notna(s["sys_blood_pressure_one"]) and pd.notna(s["sys_blood_pressure_two"]):
        return 2
    elif pd.notna(s["sys_blood_pressure_one"]) and pd.isna(s["sys_blood_pressure_two"]):
        return 1
    return 0


def get_bp_controlled_baseline(s):
    if pd.isna(s["bp_sys_baseline"]) or pd.isna(s["bp_dia_baseline"]):
        return np.nan
    elif s["bp_sys_baseline"] >= 140 or s["bp_dia_baseline"] >= 90:
        return 0
    elif s["bp_sys_baseline"] < 140 and s["bp_dia_baseline"] < 90:
        return 1
    return np.nan


def get_bp_controlled_endline(s):
    if pd.isna(s["bp_sys_endline"]) or pd.isna(s["bp_dia_endline"]):
        return np.nan
    elif s["bp_sys_endline"] >= 140 or s["bp_dia_endline"] >= 90:
        return 0
    elif s["bp_sys_endline"] < 140 and s["bp_dia_endline"] < 90:
        return 1
    return np.nan


def get_bp_severe_htn_baseline(s):
    if pd.isna(s["bp_sys_baseline"]) or pd.isna(s["bp_dia_baseline"]):
        return np.nan
    elif s["bp_sys_baseline"] >= 180 or s["bp_dia_baseline"] >= 120:
        return 1
    return 0


def get_bp_severe_htn_endline(s):
    if pd.isna(s["bp_sys_endline"]) or pd.isna(s["bp_dia_endline"]):
        return np.nan
    elif s["bp_sys_endline"] >= 180 or s["bp_dia_endline"] >= 120:
        return 1
    return 0


def get_bp_measured_interval(s):
    if pd.notna(s["bp_datetime_first"]) or pd.notna(s["bp_datetime_last"]):
        return s["bp_datetime_last"] - s["bp_datetime_first"]
    return pd.NaT


def get_bp_sys_baseline(s):
    if pd.notna(s["bp_visit_code_first"]) and s["bp_visit_code_first"] == 1000.0:
        return s["bp_systolic_first"]
    return np.nan


def get_bp_sys_endline(s):
    if pd.notna(s["bp_datetime_last"]) and (
        s["bp_datetime_last"] - s["baseline_datetime"]
    ) >= timedelta(days=182):
        return s["bp_systolic_last"]
    return np.nan


def get_bp_dia_baseline(s):
    if pd.notna(s["bp_visit_code_first"]) and s["bp_visit_code_first"] == 1000.0:
        return s["bp_diastolic_first"]
    return np.nan


def get_bp_dia_endline(s):
    if pd.notna(s["bp_datetime_last"]) and (
        s["bp_datetime_last"] - s["baseline_datetime"]
    ) >= timedelta(days=182):
        return s["bp_diastolic_last"]
    return np.nan


def merge_in_bp(df_main: pd.DataFrame) -> pd.DataFrame:
    """Need to consider duration between measurements!"""
    # TODO: Need to consider duration between measurements! what qualifies as first and last

    df_vitals = get_crf(
        model="intecomm_subject.vitals", subject_visit_model="intecomm_subject.subjectvisit"
    )
    df_vitals["bp_systolic"] = df_vitals.apply(get_systolic, axis=1)
    df_vitals["bp_measured"] = df_vitals.apply(get_bp_measured, axis=1)
    df_vitals["bp_diastolic"] = df_vitals.apply(get_diastolic, axis=1)
    df_vitals = df_vitals.sort_values(by=["subject_identifier", "visit_datetime"])
    df_vitals.rename(
        columns={"visit_datetime": "bp_datetime", "visit_code": "bp_visit_code"},
        inplace=True,
    )
    df_vitals_first_last = (
        df_vitals[
            [
                "subject_identifier",
                "bp_measured",
                "bp_visit_code",
                "bp_datetime",
                "bp_systolic",
                "bp_diastolic",
            ]
        ]
        .groupby(by=["subject_identifier"])
        .agg(["first", "last"])
        .reset_index()
    )
    df_vitals_first_last.columns = [
        "_".join(col).strip() if col[1] else col[0]
        for col in df_vitals_first_last.columns.values
    ]
    df_vitals_first_last["bp_measured_delta"] = df_vitals_first_last.apply(
        get_bp_measured_interval, axis=1
    )
    df_vitals_first_last = df_vitals_first_last[
        [
            "subject_identifier",
            # "bp_measured",
            "bp_measured_delta",
            "bp_visit_code_first",
            "bp_visit_code_last",
            "bp_datetime_first",
            "bp_datetime_last",
            "bp_systolic_first",
            "bp_systolic_last",
            "bp_diastolic_first",
            "bp_diastolic_last",
        ]
    ]
    df_vitals_first_last.reset_index(drop=True, inplace=True)

    # df_vitals_first_last.rename(
    #     columns={
    #         # "bp_systolic_first": "bp_sys_baseline",
    #         # "bp_systolic_last": "bp_sys_endline",
    #         # "bp_diastolic_first": "bp_dia_baseline",
    #         # "bp_diastolic_last": "bp_dia_endline",
    #         "bp_datetime_first": "bp_datetime_baseline",
    #         "bp_datetime_last": "bp_datetime_endline",
    #         "bp_visit_code_first": "bp_visit_code_baseline",
    #         "bp_visit_code_last": "bp_visit_code_endline",
    #     },
    #     inplace=True,
    # )

    df_main = df_main.merge(df_vitals_first_last, on="subject_identifier", how="left")
    df_main.reset_index(drop=True)
    df_main["bp_sys_baseline"] = df_main.apply(get_bp_sys_baseline, axis=1)
    df_main["bp_dia_baseline"] = df_main.apply(get_bp_dia_baseline, axis=1)
    df_main["bp_sys_endline"] = df_main.apply(get_bp_sys_endline, axis=1)
    df_main["bp_dia_endline"] = df_main.apply(get_bp_dia_endline, axis=1)
    df_main["bp_controlled_baseline"] = df_main.apply(get_bp_controlled_baseline, axis=1)
    df_main["bp_controlled_endline"] = df_main.apply(get_bp_controlled_endline, axis=1)
    df_main["bp_severe_htn_baseline"] = df_main.apply(get_bp_severe_htn_baseline, axis=1)
    df_main["bp_severe_htn_endline"] = df_main.apply(get_bp_severe_htn_endline, axis=1)
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_glucose(df_main: pd.DataFrame) -> pd.DataFrame:
    df_glucose = get_all_glucose_results(df_main)
    df_first = get_glucose_first(df_glucose)
    df_last = get_glucose_last(df_glucose)

    df_first.rename(
        columns={
            "glucose_date_first": "glucose_date_baseline",
            "glucose_value_first": "glucose_value_baseline",
            "glucose_units_first": "glucose_units_baseline",
            "glucose_fasting_duration_delta_first": "glucose_fasting_duration_delta_baseline",
            "glucose_fasting_duration_hours_first": "glucose_fasting_duration_hours_baseline",
            "glucose_date_delta_first": "glucose_date_delta_baseline",
        },
        inplace=True,
    )
    df_last.rename(
        columns={
            "glucose_date_last": "glucose_date_endline",
            "glucose_value_last": "glucose_value_endline",
            "glucose_units_last": "glucose_units_endline",
            "glucose_fasting_duration_delta_last": "glucose_fasting_duration_delta_endline",
            "glucose_fasting_duration_hours_last": "glucose_fasting_duration_hours_endline",
            "glucose_date_delta_last": "glucose_date_delta_endline",
        },
        inplace=True,
    )
    df_first_and_last = pd.merge(
        df_first, df_last, on=["subject_identifier", "baseline_datetime"], how="outer"
    )
    df_first_and_last.reset_index(drop=True, inplace=True)
    df_main = df_main.merge(
        df_first_and_last[
            [
                "subject_identifier",
                "glucose_date_baseline",
                "glucose_value_baseline",
                "glucose_units_baseline",
                "glucose_fasting_duration_delta_baseline",
                "glucose_fasting_duration_hours_baseline",
                "glucose_date_delta_baseline",
                "glucose_date_endline",
                "glucose_value_endline",
                "glucose_units_endline",
                "glucose_fasting_duration_delta_endline",
                "glucose_fasting_duration_hours_endline",
                "glucose_date_delta_endline",
            ]
        ],
        on=["subject_identifier"],
        how="left",
    )
    df_main.reset_index(drop=True, inplace=True)
    df_main["glucose_measured_days_endline"] = (
        df_main["glucose_date_endline"] - df_main["baseline_datetime"]
    ).dt.days
    df_main["glucose_measured_days_baseline"] = (
        df_main["glucose_date_baseline"] - df_main["baseline_datetime"]
    ).dt.days
    df_main["glucose_first_to_last_days"] = (
        df_main["glucose_date_endline"] - df_main["glucose_date_baseline"]
    ).dt.days

    # Glucose controlled
    df_main["glucose_controlled_baseline"] = df_main["glucose_value_baseline"].apply(
        lambda x: glucose_controlled(x)
    )
    df_main["glucose_controlled_endline"] = df_main["glucose_value_endline"].apply(
        lambda x: glucose_controlled(x)
    )
    df_main["glucose_resulted_baseline"] = df_main["glucose_value_baseline"].apply(
        lambda x: NO if pd.isna(x) else YES
    )
    df_main["glucose_resulted_endline"] = df_main["glucose_value_endline"].apply(
        lambda x: NO if pd.isna(x) else YES
    )

    df_main.reset_index(drop=True, inplace=True)
    return df_main
