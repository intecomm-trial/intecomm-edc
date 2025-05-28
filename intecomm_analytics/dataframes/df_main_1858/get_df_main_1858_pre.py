import pandas as pd
from django_pandas.io import read_frame
from edc_pdutils.dataframes import get_subject_visit
from intecomm_rando.models import RandomizationList

from ..get_patientlog_df import get_patientlog_df

BASELINE_VISIT_CODE = 1000.0

__all__ = ["get_df_main_1858_pre", "BASELINE_VISIT_CODE"]


def get_rando() -> pd.DataFrame:
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
    df_rando = (
        df_rando[df_rando.group_identifier.notna()]
        .rename(columns={"id": "randomization_list_id"})
        .reset_index(drop=True)
    )
    return df_rando


def merge_in_rando(df_main: pd.DataFrame) -> pd.DataFrame:
    """Add assignment, etc. from merge with RandomizationList.

    Note: unit of randomization is the group, not the subject."""
    df_rando = get_rando()
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


def get_df_main_1858_pre():
    """df_main_pre before merging in other CRF data.

    You can use this to merge with df_visit, parts of df_main_1868
    and any CRF if looking at all timepoints not just baseline
    and endline.

    See also `get_df_main_1858` for just baseline and endline.
    """
    # start with `patient log`
    # using patient_log is one way to link group_identifier and subject_identifier
    df_main_pre = get_patientlog_df()

    # exclude those in patient_log that were not added to a group
    df_main_pre = df_main_pre[(df_main_pre.group_identifier.notna())]

    # exclude those added to a group but never consented
    df_main_pre = df_main_pre[(df_main_pre.consent_datetime.notna())]

    assert len(df_main_pre) == 1864  # nosec B101

    # rename conditions reported at screening to distinguish from those
    # confirmed later at baseline
    df_main_pre.rename(
        columns={"hiv": "hiv_scr", "htn": "htn_scr", "dm": "dm_scr"}, inplace=True
    )
    # 1858 subjects
    df_main_pre = merge_in_rando(df_main_pre)
    df_main_pre = df_main_pre[~(df_main_pre.subject_identifier == "107-208-0014-2")]

    df_visit = get_subject_visit("intecomm_subject.subjectvisit")
    df_visit = df_visit[
        (df_visit.visit_code == BASELINE_VISIT_CODE)
        & ~(df_visit.subject_identifier == "107-208-0014-2")
    ]
    df_main_pre = df_main_pre.merge(
        df_visit[["subject_identifier"]],
        on="subject_identifier",
        how="right",
        suffixes=("", "_pre"),
    ).reset_index(drop=True)

    assert len(df_main_pre.subject_identifier.unique()) == 1858  # nosec B101

    return df_main_pre
