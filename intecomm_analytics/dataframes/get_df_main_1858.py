from pathlib import Path

import pandas as pd
from django_pandas.io import read_frame
from edc_model import duration_to_date
from edc_pdutils.dataframes import get_crf, get_subject_visit
from intecomm_rando.models import RandomizationList

from intecomm_screening.models import SubjectScreening

from .get_patientlog_df import get_patientlog_df
from .get_vl_summary import VlSummary2

__all__ = ["get_df_main_1858"]


def get_ncd(s):
    if (s["htn"] == 1 or s["dm"] == 1) and s["hiv"] == 0:
        return 1
    return 0


def get_hiv_only(s):
    if s["htn"] == 0 and s["dm"] == 0 and s["hiv"] == 1:
        return 1
    return 0


def get_dx_date(s):
    if pd.isna(s["dx_date"]) and not pd.isna(s["dx_ago"]):
        dx_calculated_date = duration_to_date(s["dx_ago"], s["visit_datetime"])
        return dx_calculated_date
    return s["dx_date"]


def get_df_main_1858(export_folder: Path | None) -> pd.DataFrame:
    # export_folder = export_folder or Path(
    #     "/Users/erikvw/Documents/ucl/protocols/intecomm/analysis/primary/"
    # )
    df = get_patientlog_df()
    df_screen = read_frame(SubjectScreening.objects.all())
    df_screen[df_screen.eligible == 1].count()
    # conditions at grouping

    df_visit = get_subject_visit("intecomm_subject.subjectvisit")
    df_visit = df_visit[
        (df_visit.visit_code == 1000.0) & ~(df_visit.subject_identifier == "107-208-0014-2")
    ]
    # merge with df_visit
    df_main = pd.merge(
        df_visit[["subject_identifier"]],
        df[(df.group_identifier.notna())],
        on="subject_identifier",
        how="left",
    )

    # 1858 subjects

    # create ncd column and hiv_only column
    df_main["ncd"] = df_main.apply(get_ncd, axis=1)
    df_main["hiv_only"] = df_main.apply(get_hiv_only, axis=1)

    # add ssignment from merge with RandomizationList
    df_rando = read_frame(
        RandomizationList.objects.values("group_identifier", "assignment").filter(
            group_identifier__isnull=False
        )
    )
    df_main = df_main.merge(
        df_rando[["group_identifier", "assignment"]], on="group_identifier", how="left"
    )

    # conditions from the baseline initial forms
    subject_identifiers = list(df_main.subject_identifier.unique())
    opts = dict(
        subject_visit_model="intecomm_subject.subjectvisit",
        subject_identifiers=subject_identifiers,
    )
    df_hiv_initial = get_crf(model="intecomm_subject.hivinitialreview", **opts)
    df_htn_initial = get_crf(model="intecomm_subject.htninitialreview", **opts)
    df_dm_initial = get_crf(model="intecomm_subject.dminitialreview", **opts)

    # recalculate dx_date if from dx_ago
    df_hiv_initial["dx_date"] = df_hiv_initial.apply(get_dx_date, axis=1)
    df_htn_initial["dx_date"] = df_htn_initial.apply(get_dx_date, axis=1)
    df_dm_initial["dx_date"] = df_dm_initial.apply(get_dx_date, axis=1)

    df_hiv_initial["hiv_timedelta_dx"] = pd.to_datetime(
        df_hiv_initial["visit_datetime"]
    ) - pd.to_datetime(df_hiv_initial["dx_date"])
    df_htn_initial["htn_timedelta_dx"] = pd.to_datetime(
        df_htn_initial["visit_datetime"]
    ) - pd.to_datetime(df_htn_initial["dx_date"])
    df_dm_initial["dm_timedelta_dx"] = pd.to_datetime(
        df_dm_initial["visit_datetime"]
    ) - pd.to_datetime(df_dm_initial["dx_date"])

    df_hiv_initial["hiv_years_since_dx"] = df_hiv_initial["hiv_timedelta_dx"].dt.days / 365
    df_htn_initial["htn_years_since_dx"] = df_htn_initial["htn_timedelta_dx"].dt.days / 365
    df_dm_initial["dm_years_since_dx"] = df_dm_initial["dm_timedelta_dx"].dt.days / 365

    df_delta = pd.merge(
        df_hiv_initial[["subject_identifier", "hiv_years_since_dx", "hiv_timedelta_dx"]],
        df_htn_initial[["subject_identifier", "htn_years_since_dx", "htn_timedelta_dx"]],
        on="subject_identifier",
        how="outer",
    )
    df_delta = df_delta.merge(
        df_dm_initial[["subject_identifier", "dm_years_since_dx", "dm_timedelta_dx"]],
        on="subject_identifier",
        how="outer",
    )

    df_main = df_main.merge(df_delta, on="subject_identifier", how="left")

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
