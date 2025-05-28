import pandas as pd
from edc_pdutils.dataframes import get_subject_visit

from ..get_location_update import get_location_update
from ..visit import get_subject_visit_missed, update_reason_unscheduled
from .get_df_main_1858 import get_df_main_1858
from .get_df_main_1858_pre import get_df_main_1858_pre

__all__ = ["get_df_main_for_crfs"]


def get_df_main_for_crfs(fasting_hours: float | None = None) -> pd.DataFrame:
    """Dataset for longitudinal anaylsis and includes
    all timepoints for each of the 1858 participants.

    Returns 20,795 rows

    Merges with df_main_1858.

    If looking at `baseline` and `endline` only, use df_main_1858
    instead.
    """

    df_main_pre = get_df_main_1858_pre()
    assert len(df_main_pre.subject_identifier.unique()) == 1858  # nosec B101

    df_visit = get_subject_visit("intecomm_subject.subjectvisit")

    df_visit = df_visit.merge(
        df_main_pre, on="subject_identifier", how="right", suffixes=("", "_right")
    ).reset_index(drop=True)

    df_visit = df_visit.drop(columns=[col for col in df_visit if col.endswith("_right")])

    assert len(df_visit.subject_identifier.unique()) == 1858  # nosec B101

    df_visit = update_reason_unscheduled(df_visit)

    df_subjectvisitmissed = get_subject_visit_missed()

    df_visit = df_visit.merge(
        df_subjectvisitmissed[["subject_visit_id", "missed_reasons"]],
        on="subject_visit_id",
        how="left",
    ).rename(columns={"missed_reasons": "reason_missed_detail"})

    df_location_update = get_location_update(df_main_pre)
    df_visit = df_visit.merge(
        df_location_update[["subject_identifier", "direction", "visit_code"]],
        how="left",
        on=["subject_identifier", "visit_code"],
    )

    df_main_1868 = get_df_main_1858(None, fasting_hours=fasting_hours)

    df_main = df_visit.merge(
        df_main_1868, how="left", on=["subject_identifier"], suffixes=("", "_right")
    )

    df_main = df_main.drop(columns=[col for col in df_main.columns if col.endswith("_right")])
    df_main = df_main.drop(
        columns=[
            "allocation",
            "allocated_datetime",
            "appointment_id",
            "randomization_list_id",
        ]
    )

    assert len(df_main.subject_identifier.unique()) == 1858  # nosec B101
    assert len(df_main) == 20795  # nosec B101

    return df_main
