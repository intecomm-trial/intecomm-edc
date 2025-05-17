from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from django_pandas.io import read_frame
from edc_constants.constants import NEVER, NO, OTHER, YES
from edc_model import duration_to_date
from edc_model_to_dataframe import read_frame_edc
from edc_pdutils.dataframes import get_crf, get_subject_visit
from edc_pdutils.utils import convert_numbers_to_nullable_dtype
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from intecomm_rando.models import RandomizationList
from pandas._libs.missing import NAType
from pandas._libs.tslibs.nattype import NaTType

from intecomm_ae.models import DeathReport
from intecomm_prn.models import EndOfStudy

from ..constants import (
    DM_ALONE,
    HIV_ALONE,
    HTN_ALONE,
    HTN_DM,
    UNDEFINED,
    primary_cohort_mapping,
)
from ..notebooks.primary.glucose import (
    get_all_glucose_results,
    get_glucose_first,
    get_glucose_last,
)
from .get_patientlog_df import get_patientlog_df
from .get_vl_summary import VlSummary2

__all__ = ["get_df_main_1858", "treatment_arm_labels"]

treatment_arm_labels = {COMMUNITY_ARM: "Community", FACILITY_ARM: "Facility"}
BASELINE_VISIT_CODE = 1000.0


def get_df_main_1858(
    export_folder: Path | None, fasting_hours: float | None = None
) -> pd.DataFrame:
    """Returns a dataframe of the population for the primary analysis.

    Removes 107-208-0014-2 (who was incorrectly registered).
    """

    # start with `patient log`
    # using patient_log is one way to link group_identifier and subject_identifier
    df_main = get_patientlog_df()

    # exclude those in patient_log that were not added to a group
    df_main = df_main[(df_main.group_identifier.notna())]

    # exclude those added to a group but never consented
    df_main = df_main[(df_main.consent_datetime.notna())]

    assert len(df_main) == 1864  # nosec B101

    # rename conditions reported at screening to distinguish from those
    # confirmed later at baseline
    df_main.rename(columns={"hiv": "hiv_scr", "htn": "htn_scr", "dm": "dm_scr"}, inplace=True)

    # merge with df_visit
    # this merge leaves us with only the subjects who presented for the
    # rando / baseline visit
    df_main = merge_in_visit(df_main)

    assert len(df_main) == 1858  # nosec B101

    # 1858 subjects
    df_main = merge_in_rando(df_main)

    assert len(df_main[df_main.assignment == "a"]) == 932  # nosec B101
    assert len(df_main[df_main.assignment == "b"]) == 926  # nosec B101
    assert len(df_main[df_main.allocation == "1"]) == 932  # nosec B101
    assert len(df_main[df_main.allocation == "2"]) == 926  # nosec B101

    # merge in baseline conditions. Conditions (hiv, dm, htn) are confirmed at baseline.
    # There is a slight difference in that reported at screening (hiv_scr, dm_scr, htn_scr)
    # from what was confirmed at baseline.
    # also note, for a condition must be diagnosed more than 6m ago
    df_main = merge_in_baseline_conditions(df_main)

    # create ncd column and hiv_only column
    df_main["ncd"] = df_main.apply(get_ncd, axis=1)
    df_main["hiv_only"] = df_main.apply(get_hiv_only, axis=1)
    df_main["htn_only"] = df_main.apply(get_htn_only, axis=1)
    df_main["dm_only"] = df_main.apply(get_dm_only, axis=1)
    df_main["htn_and_dm"] = df_main.apply(get_htn_and_dm, axis=1)
    df_main["hiv_and_htn_and_dm"] = df_main.apply(get_hiv_htn_and_dm, axis=1)

    df_main = merge_in_vitals(df_main)

    df_main = merge_in_other_baseline_data(df_main)

    df_main = merge_in_complications(df_main)

    df_main = merge_in_vl(df_main)

    df_main = merge_in_eos(df_main)

    df_main = merge_death_report(df_main)

    df_main["onstudy_days"] = (df_main.endline_datetime - df_main.baseline_datetime).dt.days

    df_main = merge_in_bp(df_main)

    df_main = merge_in_glucose(df_main, fasting_hours=fasting_hours)

    df_main["country"] = df_main.apply(get_country, axis=1)

    df_main = merge_in_pp_using_location_update_crf(df_main)

    df_main = merge_in_primary_cohort_vars(df_main, fasting_hours=fasting_hours)

    df_main["years_since_dx"] = df_main.apply(get_years_since_dx, axis=1)

    # flag rows for endline analysis
    df_main["endline"] = 0
    df_main.loc[
        (df_main.offstudy_reason == "completed_followup")
        & (df_main.primary_cohort != UNDEFINED),
        "endline",
    ] = 1

    # for simplicity, clear out endline cols values where endline==0
    datecols = df_main.dtypes[df_main.dtypes == "datetime64[ns]"].index.tolist()
    cols = df_main.dtypes[df_main.dtypes != "datetime64[ns]"].index.tolist()
    df_main.loc[df_main.endline == 0, [col for col in datecols if "endline" in col]] = pd.NaT
    df_main.loc[df_main.endline == 0, [col for col in cols if "endline" in col]] = pd.NA

    assert len(df_main) == 1858  # nosec B101

    if export_folder:
        df_main.to_csv(
            Path(export_folder) / "df_main_1858.csv",
            index=False,
        )
    return df_main


def glucose_controlled(value):
    if pd.notna(value):
        if value < 7.00:
            return 1
        elif value >= 7.00:
            return 0
    return pd.NA


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


def get_htn_and_dm(s):
    if s["htn"] == 1 and s["dm"] == 1 and s["hiv"] == 0:
        return 1
    return 0


def get_hiv_htn_and_dm(s):
    if s["htn"] == 1 and s["dm"] == 1 and s["hiv"] == 1:
        return 1
    return 0


def get_primary_cohort(s) -> None | int:
    """Derived column for `primary` cohorts"""
    if s["htn"] == 0 and s["dm"] == 1 and s["hiv"] == 0:
        return DM_ALONE
    elif s["htn"] == 1 and s["dm"] == 0 and s["hiv"] == 0:
        return HTN_ALONE
    elif s["htn"] == 1 and s["dm"] == 1 and s["hiv"] == 0:
        return HTN_DM
    elif s["htn"] == 0 and s["dm"] == 0 and s["hiv"] == 1:
        return HIV_ALONE
    return UNDEFINED


def get_primary_cohort_as_str(s) -> None | str:
    """Derived column for `primary` cohorts"""
    if s["primary_cohort"] in primary_cohort_mapping:
        return primary_cohort_mapping[s["primary_cohort"]]
    return None


def _controlled(s, timepoint):
    """Same as controlled() but differs from SAP to accept control
    in one condition as controlled
    """
    value = pd.NA
    if pd.notna(s["primary_cohort_str"]):
        if s.primary_cohort_str == "HTN_ALONE":
            return getattr(s, f"bp_controlled_{timepoint}")
        elif s.primary_cohort_str == "DM_ALONE":
            return getattr(s, f"glucose_controlled_{timepoint}")
        elif s.primary_cohort_str == "HTN_DM":
            if pd.isna(getattr(s, f"bp_controlled_{timepoint}")) and pd.isna(
                getattr(s, f"glucose_controlled_{timepoint}")
            ):
                value = pd.NA
            else:
                s64 = pd.Series(s, dtype="Int64")
                bp = getattr(s64, f"bp_controlled_{timepoint}")
                gl = getattr(s64, f"glucose_controlled_{timepoint}")
                bp = 0 if pd.isna(bp) else bp
                gl = 0 if pd.isna(gl) else gl
                value = bp + gl
                # must be controlled in both to be controlled
                value = 1 if value == 2 else 0
        elif s.primary_cohort_str == "HIV_ALONE":
            value = getattr(s, f"vl_controlled_{timepoint}")
    return value


def _controlled_alt(s, timepoint):
    """Same as controlled() but differs from SAP to accept control
    in one condition as controlled
    """
    value = pd.NA
    if pd.notna(s["primary_cohort_str"]):
        if s.primary_cohort_str == "HTN_ALONE":
            return getattr(s, f"bp_controlled_{timepoint}")
        elif s.primary_cohort_str == "DM_ALONE":
            return getattr(s, f"glucose_controlled_{timepoint}")
        elif s.primary_cohort_str == "HTN_DM":
            if pd.isna(getattr(s, f"bp_controlled_{timepoint}")) and pd.isna(
                getattr(s, f"glucose_controlled_{timepoint}")
            ):
                value = pd.NA
            else:
                s64 = pd.Series(s, dtype="Int64")
                bp = getattr(s64, f"bp_controlled_{timepoint}")
                gl = getattr(s64, f"glucose_controlled_{timepoint}")
                bp = 0 if pd.isna(bp) else bp
                gl = 0 if pd.isna(gl) else gl
                value = bp + gl
                # different from _controlled! Only need control in one.
                value = 1 if value in [1, 2] else 0
        elif s.primary_cohort_str == "HIV_ALONE":
            value = getattr(s, f"vl_controlled_{timepoint}")
    return value


def controlled_baseline(s):
    return _controlled(s, timepoint="baseline")


def controlled_endline(s):
    return _controlled(s, timepoint="endline")


def controlled_baseline_alt(s):
    """Same as controlled_baseline but differs from SAP to accept control
    in one condition as controlled

    Cases are written out explicitly
    """
    return _controlled_alt(s, timepoint="baseline")


def controlled_endline_alt(s):
    """Same as controlled_baseline but differs from SAP to accept control
    in one condition as controlled

    Cases are written out explicitly
    """
    return _controlled_alt(s, timepoint="endline")


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
        "hiv",
        "dm",
        "htn",
        "hiv_only",
        "dm_only",
        "htn_only",
        "htn_and_dm",
        "ncd",
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


def categorize_offstudy_reason_freetext(df_main: pd.DataFrame) -> pd.DataFrame:
    """Categorize offstudy_reason free text."""
    df_main["offstudy_reason_raw"] = df_main["offstudy_reason"]
    reasons = (
        df_main[
            ~(
                df_main.offstudy_reason.isin(
                    [
                        "completed_followup",
                        "LTFU",
                        "transferred",
                        "consent_withdrawal",
                        "dead",
                        "clinical_withdrawal",
                    ]
                )
            )
        ]
        .offstudy_reason.value_counts()
        .to_frame()
        .index.tolist()
    )
    pregnant_reason = reasons.pop(
        reasons.index(
            "Patient  is pregnant Reffered to Pmtct clinic on 14/03/2024 for further "
            "maternal and child care."
        )
    )
    df_main.loc[
        df_main.offstudy_reason_raw.str.startswith(pregnant_reason), "offstudy_reason"
    ] = "pregnant"
    for reason in reasons:
        df_main.loc[df_main.offstudy_reason_raw.str.startswith(reason), "offstudy_reason"] = (
            "transferred"
        )
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_visit(df_main: pd.DataFrame) -> pd.DataFrame:
    """Merge in visit.

    Assume if visit 1000 exists => patient is on trial.

    Remove 107-208-0014-2 (incorrectly registered)
    """

    df_visit = get_subject_visit("intecomm_subject.subjectvisit")
    df_visit = df_visit[
        (df_visit.visit_code == BASELINE_VISIT_CODE)
        & ~(df_visit.subject_identifier == "107-208-0014-2")
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
    """Add assignment, etc. from merge with RandomizationList.

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


def merge_death_report(df_main: pd.DataFrame) -> pd.DataFrame:
    df = read_frame_edc(DeathReport.objects.all(), read_frame_verbose=False)
    df.rename(
        columns={"death_datetime": "death_date_from_crf", "cause_of_death": "death_cause"},
        inplace=True,
    )
    df["death_date_from_crf"] = df["death_date_from_crf"].astype("datetime64[ns]")
    df_main = df_main.merge(
        df[["subject_identifier", "death_cause", "death_date_from_crf"]],
        on="subject_identifier",
        how="left",
    )
    df_main["death_days_to_event"] = (
        df_main.death_date_from_crf - df_main.baseline_datetime
    ).dt.days
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_eos(df_main: pd.DataFrame) -> pd.DataFrame:
    """Merge in eos / offstudy"""
    df_eos = read_frame_edc(EndOfStudy.objects.all(), read_frame_verbose=False)
    df_eos["offstudy_reason"] = df_eos.apply(get_offstudy_reason, axis=1)
    df_eos.drop(columns=["offstudy_reason_name"], inplace=True)
    df_eos["endline_datetime"] = df_eos["offstudy_datetime"]
    for col in [
        "offstudy_datetime",
        "endline_datetime",
        "death_date",
        "transfer_date",
        "ltfu_date",
    ]:
        df_eos[col] = df_eos[col].astype("datetime64[ns]")
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
    df_main = categorize_offstudy_reason_freetext(df_main)
    df_main.loc[df_main.offstudy_reason == "transferred", "transferred_days_to_event"] = (
        df_main.transfer_date - df_main.baseline_datetime
    ).dt.days
    df_main.loc[df_main.offstudy_reason == "LTFU", "ltfu_days_to_event"] = (
        df_main.ltfu_date - df_main.baseline_datetime
    ).dt.days
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_vl(df_main: pd.DataFrame) -> pd.DataFrame:
    vl = VlSummary2(
        offset_by="days", baseline_upper=61, endline_upper=182, skip_update_dx=True
    )
    df_vl = vl.to_dataframe()

    df_vl = convert_numbers_to_nullable_dtype(df_vl)

    df_vl.drop(
        columns=[
            "vl_baseline_value",
            "vl_baseline_date",
            "vl_endline_value",
            "vl_endline_date",
        ],
        inplace=True,
    )
    df_vl.rename(
        columns={
            "baseline_vl": "vl_baseline",
            "endline_vl": "vl_endline",
            "baseline_vl_date": "vl_baseline_date",
            "endline_vl_date": "vl_endline_date",
        },
        inplace=True,
    )

    df_main = df_main.merge(
        df_vl[
            [
                "subject_identifier",
                "vl_baseline",
                "vl_baseline_date",
                "vl_endline",
                "vl_endline_date",
            ]
        ],
        on="subject_identifier",
        how="left",
    )
    for timepoint in ["baseline", "endline"]:
        df_main[f"vl_controlled_{timepoint}"] = getattr(df_main, f"vl_{timepoint}").apply(
            lambda x: 1 if x < 1000 else 0
        )
        df_main[f"vl_controlled_{timepoint}_400"] = getattr(df_main, f"vl_{timepoint}").apply(
            lambda x: 1 if x < 400 else 0
        )
        df_main[f"vl_controlled_{timepoint}_50"] = getattr(df_main, f"vl_{timepoint}").apply(
            lambda x: 1 if x < 50 else 0
        )
        df_main[f"vl_{timepoint}_log10"] = getattr(df_main, f"vl_{timepoint}").apply(
            lambda x: np.log10(x)
        )

    df_main["vl_days_to_event"] = (df_main.vl_endline_date - df_main.baseline_datetime).dt.days
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

    df_hiv_initial["hiv_years_since_dx"] = df_hiv_initial[
        "hiv_timedelta_dx"
    ].dt.total_seconds() / (365.25 * 24 * 3600)
    df_hiv_initial["hiv"] = 1
    df_htn_initial["htn_years_since_dx"] = df_htn_initial[
        "htn_timedelta_dx"
    ].dt.total_seconds() / (365.25 * 24 * 3600)
    df_htn_initial["htn"] = 1
    df_dm_initial["dm_years_since_dx"] = df_dm_initial[
        "dm_timedelta_dx"
    ].dt.total_seconds() / (365.25 * 24 * 3600)
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


def get_years_since_dx(r) -> pd.DataFrame:
    if r.primary_cohort == HIV_ALONE:
        return r.hiv_years_since_dx
    elif r.primary_cohort == DM_ALONE:
        return r.dm_years_since_dx
    elif r.primary_cohort == HTN_ALONE:
        return r.htn_years_since_dx
    elif r.primary_cohort == HTN_DM:
        return max(r.htn_years_since_dx, r.dm_years_since_dx)
    else:
        return max(
            val
            for val in [r.hiv_years_since_dx, r.htn_years_since_dx, r.dm_years_since_dx]
            if pd.notna(val)
        )


def get_diastolic(s) -> int | float | NAType:
    """Returns avg of measurement one and two. If only have
    measurement one, use that.
    """
    if pd.notna(get_systolic(s)):
        if pd.notna(s["dia_blood_pressure_one"]) and pd.notna(s["dia_blood_pressure_two"]):
            return s["dia_blood_pressure_avg"]
        elif pd.notna(s["dia_blood_pressure_one"]) and pd.isna(s["dia_blood_pressure_two"]):
            return s["dia_blood_pressure_one"]
    return pd.NA


def get_systolic(s) -> int | float | NAType:
    """Returns avg of measurement one and two. If only have
    measurement one, use that.
    """
    if pd.notna(s["sys_blood_pressure_one"]) and pd.notna(s["sys_blood_pressure_two"]):
        return s["sys_blood_pressure_avg"]
    elif pd.notna(s["sys_blood_pressure_one"]) and pd.isna(s["sys_blood_pressure_two"]):
        return s["sys_blood_pressure_one"]
    return pd.NA


def get_bp_measured(s) -> int:
    """2=two readings, 1=one reading, 0=no readings"""
    if pd.notna(s["sys_blood_pressure_one"]) and pd.notna(s["sys_blood_pressure_two"]):
        return 2
    elif pd.notna(s["sys_blood_pressure_one"]) and pd.isna(s["sys_blood_pressure_two"]):
        return 1
    return 0


def get_bp_controlled_baseline(s) -> int | float | NAType:
    """1=Controlled, 0=uncontrolled"""
    if pd.isna(s["bp_sys_baseline"]) or pd.isna(s["bp_dia_baseline"]):
        return pd.NA
    elif s["bp_sys_baseline"] >= 140 or s["bp_dia_baseline"] >= 90:
        return 0
    elif s["bp_sys_baseline"] < 140 and s["bp_dia_baseline"] < 90:
        return 1
    return pd.NA


def get_bp_controlled_endline(s) -> int | float | NAType:
    """1 = Controlled, 0 = uncontrolled"""
    if pd.isna(s["bp_sys_endline"]) or pd.isna(s["bp_dia_endline"]):
        return pd.NA
    elif s["bp_sys_endline"] >= 140 or s["bp_dia_endline"] >= 90:
        return 0
    elif s["bp_sys_endline"] < 140 and s["bp_dia_endline"] < 90:
        return 1
    return pd.NA


def get_bp_severe_htn_baseline(s) -> int | float | NAType:
    """1=Severe HTN, 0=not severe"""
    if pd.isna(s["bp_sys_baseline"]) or pd.isna(s["bp_dia_baseline"]):
        return pd.NA
    elif s["bp_sys_baseline"] >= 180 or s["bp_dia_baseline"] >= 120:
        return 1
    return 0


def get_bp_severe_htn_endline(s) -> int | float | NAType:
    """1=Severe HTN, 0=not severe"""
    if pd.isna(s["bp_sys_endline"]) or pd.isna(s["bp_dia_endline"]):
        return pd.NA
    elif s["bp_sys_endline"] >= 180 or s["bp_dia_endline"] >= 120:
        return 1
    return 0


def get_bp_measured_interval(s) -> datetime | NaTType:
    if pd.notna(s["bp_datetime_first"]) or pd.notna(s["bp_datetime_last"]):
        return s["bp_datetime_last"] - s["bp_datetime_first"]
    return pd.NaT


def get_bp_sys_baseline(s) -> int | float | NAType:
    if pd.notna(s["bp_visit_code_first"]) and s["bp_visit_code_first"] == BASELINE_VISIT_CODE:
        return s["bp_systolic_first"]
    return pd.NA


def get_bp_sys_endline(s) -> int | float | NAType:
    if pd.notna(s["bp_datetime_last"]) and (
        s["bp_datetime_last"] - s["baseline_datetime"]
    ) >= timedelta(days=182):
        return s["bp_systolic_last"]
    return pd.NA


def get_bp_dia_baseline(s) -> int | float | NAType:
    if pd.notna(s["bp_visit_code_first"]) and s["bp_visit_code_first"] == BASELINE_VISIT_CODE:
        return s["bp_diastolic_first"]
    return pd.NA


def get_bp_dia_endline(s) -> int | float | NAType:
    if pd.notna(s["bp_datetime_last"]) and (
        s["bp_datetime_last"] - s["baseline_datetime"]
    ) >= timedelta(days=182):
        return s["bp_diastolic_last"]
    return pd.NA


def merge_in_vitals(df_main: pd.DataFrame) -> pd.DataFrame:

    df_vitals = get_crf(
        model="intecomm_subject.vitals", subject_visit_model="intecomm_subject.subjectvisit"
    )
    df_vitals = convert_numbers_to_nullable_dtype(df_vitals)
    df_weight = df_vitals.sort_values(by=["subject_identifier", "visit_datetime"])
    df_weight = (
        df_weight[(df_weight.weight.notna())][["subject_identifier", "weight"]]
        .groupby("subject_identifier")
        .agg(["first"])
        .reset_index()
    )
    df_weight.columns = ["subject_identifier", "weight"]
    df_main = df_main.merge(df_weight, on="subject_identifier", how="left")
    df_main.reset_index(drop=True, inplace=True)

    df_height = df_vitals.sort_values(by=["subject_identifier", "visit_datetime"])
    df_height = (
        df_height[(df_height.height.notna())][["subject_identifier", "height"]]
        .groupby("subject_identifier")
        .agg(["first"])
        .reset_index()
    )
    df_height.columns = ["subject_identifier", "height"]
    df_main = df_main.merge(df_height, on="subject_identifier", how="left")
    df_main["bmi"] = (df_main["weight"]) / ((df_main["height"] / 100) ** 2)
    df_main.reset_index(drop=True, inplace=True)

    return df_main


def merge_in_complications(df_main: pd.DataFrame) -> pd.DataFrame:
    df = get_crf(
        "intecomm_subject.complicationsbaseline",
        subject_visit_model="intecomm_subject.subjectvisit",
        read_verbose=False,
    )
    df = convert_numbers_to_nullable_dtype(df)
    df = df.rename(
        columns={
            "stroke": "complication_stroke",
            "heart_attack": "complication_heart_attack",
            "renal_disease": "complication_renal_disease",
            "vision": "complication_vision",
            "numbness": "complication_numbness",
            "foot_ulcers": "complication_foot_ulcers",
        }
    )
    df_main = df_main.merge(
        df[
            [
                "subject_identifier",
                "complication_stroke",
                "complication_heart_attack",
                "complication_renal_disease",
                "complication_vision",
                "complication_numbness",
                "complication_foot_ulcers",
            ]
        ],
        on="subject_identifier",
        how="left",
    )
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_other_baseline_data(df_main: pd.DataFrame) -> pd.DataFrame:
    df = get_crf(
        "intecomm_subject.otherbaselinedata",
        subject_visit_model="intecomm_subject.subjectvisit",
        read_verbose=False,
    )
    df = convert_numbers_to_nullable_dtype(df)
    df["alcohol_consumption"] = df["alcohol_consumption"].apply(
        lambda x: NEVER if x == "Not applicable" else x
    )
    df_main = df_main.merge(
        df[
            [
                "subject_identifier",
                "employment_status",
                "education",
                "marital_status",
                "smoking_status",
                "alcohol_consumption",
            ]
        ],
        on="subject_identifier",
        how="left",
    )
    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_bp(df_main: pd.DataFrame) -> pd.DataFrame:
    """Need to consider duration between measurements!"""
    # TODO: Need to consider duration between measurements! what qualifies as first and last

    df_vitals = get_crf(
        model="intecomm_subject.vitals", subject_visit_model="intecomm_subject.subjectvisit"
    )
    df_vitals = convert_numbers_to_nullable_dtype(df_vitals)
    df_vitals["bp_systolic"] = df_vitals.apply(get_systolic, axis=1).astype("Float64")
    df_vitals["bp_measured"] = df_vitals.apply(get_bp_measured, axis=1).astype("Float64")
    df_vitals["bp_diastolic"] = df_vitals.apply(get_diastolic, axis=1).astype("Float64")
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
    df_main = df_main.merge(df_vitals_first_last, on="subject_identifier", how="left")
    df_main.reset_index(drop=True)
    df_main["bp_sys_baseline"] = df_main.apply(get_bp_sys_baseline, axis=1).astype("Float64")
    df_main["bp_dia_baseline"] = df_main.apply(get_bp_dia_baseline, axis=1).astype("Float64")
    df_main["bp_sys_endline"] = df_main.apply(get_bp_sys_endline, axis=1).astype("Float64")
    df_main["bp_dia_endline"] = df_main.apply(get_bp_dia_endline, axis=1).astype("Float64")
    df_main["bp_controlled_baseline"] = df_main.apply(
        get_bp_controlled_baseline, axis=1
    ).astype("Int64")
    df_main["bp_controlled_endline"] = df_main.apply(get_bp_controlled_endline, axis=1).astype(
        "Int64"
    )
    df_main["bp_severe_htn_baseline"] = df_main.apply(
        get_bp_severe_htn_baseline, axis=1
    ).astype("Int64")
    df_main["bp_severe_htn_endline"] = df_main.apply(get_bp_severe_htn_endline, axis=1).astype(
        "Int64"
    )

    df_main["bp_days_to_event"] = (
        df_main.bp_datetime_last - df_main.baseline_datetime
    ).dt.days

    cond = (df_main.bp_datetime_last - df_main.baseline_datetime).dt.days < 182
    df_main.loc[cond, "bp_sys_endline"] = pd.NA
    df_main.loc[cond, "bp_dia_endline"] = pd.NA
    df_main.loc[cond, "bp_controlled_endline"] = pd.NA
    df_main.loc[cond, "bp_severe_htn_endline"] = pd.NA
    df_main.loc[cond, "bp_days_to_event"] = pd.NA

    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_glucose(
    df_main: pd.DataFrame,
    fasting_hours: float | None = None,
) -> pd.DataFrame:
    # fasting_hours = default_fasting_hours if fasting_hours is None else fasting_hours
    df_glucose = get_all_glucose_results(df_main, fasting_hours=fasting_hours)
    df_glucose = convert_numbers_to_nullable_dtype(df_glucose)

    df_first = get_glucose_first(
        df_glucose,
        # baseline_lower_bound=-182,
        # baseline_upper_bound=182,
    )
    df_last = get_glucose_last(df_glucose, endline_lower_bound=182)

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

    df_main = convert_numbers_to_nullable_dtype(df_main)

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
    df_main["glucose_controlled_baseline"] = (
        df_main["glucose_value_baseline"]
        .apply(lambda x: glucose_controlled(x))
        .astype("Int64")
    )
    df_main["glucose_controlled_endline"] = (
        df_main["glucose_value_endline"].apply(lambda x: glucose_controlled(x)).astype("Int64")
    )
    df_main["glucose_resulted_baseline"] = (
        df_main["glucose_value_baseline"]
        .apply(lambda x: 0 if pd.isna(x) else 1)
        .astype("Int64")
    )
    df_main["glucose_resulted_endline"] = (
        df_main["glucose_value_endline"]
        .apply(lambda x: 0 if pd.isna(x) else 1)
        .astype("Int64")
    )

    df_main["glucose_days_to_event"] = (
        df_main.glucose_date_endline - df_main.baseline_datetime
    ).dt.days.astype("Int64")

    df_main.reset_index(drop=True, inplace=True)
    return df_main


def get_location_update(df_main: pd.DataFrame) -> pd.DataFrame:
    """Model LocationUpdate was required when appointment.appt_type
    (community or facility) conflicted with the randomization
    assignment (a=comm, b=facility).

    The CRF validates appt_type. Initially the CRF was always required
    and later only of values conflicted. You will see 'direction' as
    a->a, b->b -- in these cases the CRF did not need to be completed.

    You will also see a few b->a which is not possible. These are
    data entry errors.

    The case of interest is a->b.
    """

    def get_direction(s):
        if s.location == OTHER:
            return OTHER
        return f"{s.assignment}->{s.location}"

    def is_before_6m(s):
        if (s.report_datetime - s.baseline_datetime).days < 182:
            return 1
        return 0

    # location update CRF was completed when appt_type did not match assignment
    df_location_update = get_crf(
        "intecomm_subject.locationupdate",
        subject_visit_model="intecomm_subject.subjectvisit",
        read_verbose=False,
    )
    # map location to assignment
    df_location_update["location"] = df_location_update["location"].map(
        {"community": COMMUNITY_ARM, "clinic": FACILITY_ARM, OTHER: OTHER}
    )
    # was subject expected to return to community. Even though often replied
    # NO, subject still returned. Can ignore this column
    df_location_update.rename(columns={"next_location": "returning"}, inplace=True)
    # merge in vars from df_main
    df_location_update = df_location_update.merge(
        df_main[["subject_identifier", "assignment", "hiv", "dm", "htn", "country"]],
        how="left",
        on="subject_identifier",
    )
    # create new column 'direction' a->a, b->b or a->b
    df_location_update["direction"] = df_location_update.apply(get_direction, axis=1)
    # was the location update CRF submitted on or before 6m
    df_location_update["<182"] = df_location_update.apply(is_before_6m, axis=1)
    # get rid of "a->a", "b->b", "OTHER", CRF should not have been completed
    df_location_update = df_location_update[
        ~df_location_update.direction.isin(["a->a", "b->b", "OTHER"])
    ].copy()
    # baseline and endline visit are at facility regardless of assignment
    # remove them
    df_location_update = df_location_update[
        (df_location_update.visit_code > 1000.0) & (df_location_update.visit_code < 1120.0)
    ].copy()

    df_location_update.sort_values(
        by=["subject_identifier", "visit_code"], ascending=[True, True], inplace=True
    )
    df_location_update.reset_index(drop=True, inplace=True)
    return df_location_update


def merge_in_pp_using_location_update_crf(df_main) -> pd.DataFrame:
    """Per protocol column, a/b"""

    df_location_update = get_location_update(df_main)

    df_main["pp"] = df_main["assignment"]

    # filter for all visits if any 6m changes from a->b
    df = df_location_update[
        (
            df_location_update.subject_identifier.isin(
                df_location_update[
                    (df_location_update.direction == "a->b")
                    & (df_location_update.visit_code == 1060.0)
                ].subject_identifier
            )
        )
        & (df_location_update.visit_code >= 1060.0)
    ].copy()
    df.sort_values(
        by=["subject_identifier", "visit_code"], ascending=[True, True], inplace=True
    )
    df.reset_index(drop=True, inplace=True)

    # of those, is there more than one visit beyond 6m?
    df = df.groupby(by=["subject_identifier"]).filter(lambda x: len(x) > 1)
    df.sort_values(
        by=["subject_identifier", "visit_code"], ascending=[True, True], inplace=True
    )
    df.reset_index(drop=True, inplace=True)
    df_main.loc[df_main.subject_identifier.isin(df.subject_identifier), "pp"] = "b"

    # now look before 6m, and update any with all 5 visits are a->b
    df = (
        df_location_update[df_location_update["<182"] == 1]
        .groupby(by=["subject_identifier"])
        .nunique()[["visit_code"]]
        .reset_index()
    )
    df_main.loc[
        df_main.subject_identifier.isin(df[df.visit_code >= 5].subject_identifier), "pp"
    ] = "b"

    df_main.reset_index(drop=True, inplace=True)
    return df_main


def merge_in_primary_cohort_vars(df_main, fasting_hours: float = None) -> pd.DataFrame:
    df_main["primary_cohort"] = df_main.apply(get_primary_cohort, axis=1).astype("Int64")
    df_main["primary_cohort_str"] = df_main.apply(get_primary_cohort_as_str, axis=1)

    for suffix in ["baseline", "endline"]:
        # glu
        column_name = f"primary_gl_{suffix}"
        df_main[column_name] = df_main[
            (df_main.primary_cohort.isin([DM_ALONE, HTN_DM]))
            & (getattr(df_main, f"glucose_fasting_duration_hours_{suffix}") >= fasting_hours)
        ][f"glucose_value_{suffix}"].astype("Float64")
        df_main.loc[~df_main.primary_cohort.isin([DM_ALONE, HTN_DM]), column_name] = pd.NA
        df_main.loc[df_main[column_name].isna(), column_name] = pd.NA

        column_name = f"primary_gl_controlled_{suffix}"
        df_main[column_name] = df_main[df_main.primary_cohort.isin([DM_ALONE, HTN_DM])][
            f"glucose_controlled_{suffix}"
        ].astype("Int64")
        df_main.loc[~df_main.primary_cohort.isin([DM_ALONE, HTN_DM]), column_name] = pd.NA
        df_main.loc[df_main[column_name].isna(), column_name] = pd.NA

        # bp
        column_name = f"primary_bp_sys_{suffix}"
        df_main[column_name] = df_main[df_main.primary_cohort.isin([HTN_ALONE, HTN_DM])][
            f"bp_sys_{suffix}"
        ].astype("Float64")
        df_main.loc[~df_main.primary_cohort.isin([HTN_ALONE, HTN_DM]), column_name] = pd.NA
        df_main.loc[df_main[column_name].isna(), column_name] = pd.NA

        column_name = f"primary_bp_dia_{suffix}"
        df_main[column_name] = df_main[df_main.primary_cohort.isin([HTN_ALONE, HTN_DM])][
            f"bp_dia_{suffix}"
        ].astype("Float64")
        df_main.loc[~df_main.primary_cohort.isin([HTN_ALONE, HTN_DM]), column_name] = pd.NA
        df_main.loc[df_main[column_name].isna(), column_name] = pd.NA

        column_name = f"primary_bp_controlled_{suffix}"
        df_main[column_name] = df_main[df_main.primary_cohort.isin([HTN_ALONE, HTN_DM])][
            f"bp_controlled_{suffix}"
        ].astype("Int64")
        df_main.loc[~df_main.primary_cohort.isin([HTN_ALONE, HTN_DM]), column_name] = pd.NA
        df_main.loc[df_main[column_name].isna(), column_name] = pd.NA

        # vl
        column_name = f"primary_vl_{suffix}"
        df_main[column_name] = df_main[df_main.primary_cohort.isin([HIV_ALONE])][
            f"vl_{suffix}"
        ].astype("Float64")
        df_main.loc[~df_main.primary_cohort.isin([HIV_ALONE]), column_name] = pd.NA
        df_main.loc[df_main[column_name].isna(), column_name] = pd.NA

        for copies_ml in ["", "_400", "_50"]:
            column_name = f"primary_vl_controlled_{suffix}{copies_ml}"
            df_main[column_name] = df_main[df_main.primary_cohort.isin([HIV_ALONE])][
                f"vl_controlled_{suffix}{copies_ml}"
            ].astype("Float64")
            df_main.loc[~df_main.primary_cohort.isin([HIV_ALONE]), column_name] = pd.NA
            df_main.loc[df_main[column_name].isna(), column_name] = pd.NA

    df_main["controlled_baseline"] = df_main.apply(controlled_baseline, axis=1).astype("Int64")
    df_main["controlled_endline"] = df_main.apply(controlled_endline, axis=1).astype("Int64")

    df_main["controlled_alt_baseline"] = df_main.apply(controlled_baseline_alt, axis=1).astype(
        "Int64"
    )
    df_main["controlled_alt_endline"] = df_main.apply(controlled_endline_alt, axis=1).astype(
        "Int64"
    )

    for suffix in ["baseline", "endline"]:
        df_main[f"primary_composite_{suffix}"] = pd.NA
        df_main.loc[
            df_main.primary_cohort.isin([HTN_ALONE, DM_ALONE, HTN_DM]),
            f"primary_composite_{suffix}",
        ] = df_main[f"controlled_{suffix}"]
        df_main[f"primary_composite_{suffix}"] = df_main[f"primary_composite_{suffix}"].astype(
            "Int64"
        )

        # alternative calc allowing control in one to be controlled
        df_main[f"primary_composite_alt_{suffix}"] = pd.NA
        df_main.loc[
            df_main.primary_cohort.isin([HTN_ALONE, DM_ALONE, HTN_DM]),
            f"primary_composite_alt_{suffix}",
        ] = df_main[f"controlled_alt_{suffix}"]
        df_main[f"primary_composite_alt_{suffix}"] = df_main[
            f"primary_composite_alt_{suffix}"
        ].astype("Int64")

    df_main.reset_index(drop=True, inplace=True)
    return df_main


def categorical_columns():
    return [
        ("hiv", {1: YES, 0: NO}),
        ("dm", {1: YES, 0: NO}),
        ("htn", {1: YES, 0: NO}),
        ("hiv_only", {1: YES, 0: NO}),
        ("dm_only", {1: YES, 0: NO}),
        ("htn_only", {1: YES, 0: NO}),
        ("htn_and_dm", {1: YES, 0: NO}),
        ("ncd", {1: YES, 0: NO}),
        "site",
        "gender",
        "stable",
        "willing_to_screen",
        "screening_refusal_reason",
        "assignment",
        "allocation",
        "stable",
        "willing_to_screen",
        "screening_refusal_reason",
        # "bp_measured",
        "employment_status",
        "education",
        "marital_status",
        "smoking_status",
        "alcohol_consumption",
        "stroke",
        "heart_attack",
        "renal_disease",
        "vision",
        "numbness",
        "foot_ulcers",
    ]
