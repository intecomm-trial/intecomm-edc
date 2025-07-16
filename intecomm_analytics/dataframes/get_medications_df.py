import pandas as pd

from .rx import (
    get_dm_rx_crf,
    get_dm_rx_variable_labels,
    get_hiv_rx_crf,
    get_hiv_rx_variable_labels,
    get_htn_rx_crf,
    get_htn_rx_variable_labels,
)


def get_medications_df() -> tuple[pd.DataFrame, dict[str:str]]:
    """Create a DF of medications (DM, HTN, HIV) merged with df_appt.

    Remember to merge on `appointment_id` and not subject_visit_id!
    """
    variable_labels = {}

    df_dm_rx = get_dm_rx_crf("dm")
    dm_cols = [col for col in df_dm_rx if col.startswith("dm_") or col == "subject_visit_id"]
    variable_labels.update(**get_dm_rx_variable_labels(df_dm_rx))

    df_htn_rx = get_htn_rx_crf("htn")
    htn_cols = [
        col for col in df_htn_rx if col.startswith("htn_") or col == "subject_visit_id"
    ]
    variable_labels.update(**get_htn_rx_variable_labels(df_htn_rx))

    df_hiv_rx = get_hiv_rx_crf()
    hiv_cols = [
        col for col in df_hiv_rx if col.startswith("hiv_") or col == "subject_visit_id"
    ]
    variable_labels.update(**get_hiv_rx_variable_labels(df_hiv_rx))

    df_meds = pd.merge(
        df_dm_rx[dm_cols],
        df_htn_rx[htn_cols],
        on="subject_visit_id",
        how="outer",
        suffixes=("", "_y"),
    )
    df_meds = pd.merge(
        df_meds, df_hiv_rx[hiv_cols], on="subject_visit_id", how="outer", suffixes=("", "_y")
    )
    df_meds = df_meds.astype(
        {col: "Float64" for col in df_meds.select_dtypes(include=["float", "float64"]).columns}
    )
    df_meds = df_meds.astype(
        {col: "Int64" for col in df_meds.select_dtypes(include=["int", "int64"]).columns}
    )
    df_meds = df_meds.astype(
        {
            col: "datetime64[ns]"
            for col in df_meds.select_dtypes(include=["datetime", "datetime64"]).columns
        }
    )
    df_meds = df_meds.fillna(pd.NA)

    df_meds = df_meds.rename(
        columns={
            "htn_rx_modifications_reason_other": "htn_rx_mod_reason_other",
            "hiv_rx_modifications_reason_other": "hiv_rx_mod_reason_other",
            "dm_rx_modifications_reason_other": "dm_rx_mod_reason_other",
        }
    )

    assert (
        len(
            df_meds[
                (df_meds["subject_visit_id"].duplicated(keep=False))
                & (df_meds["subject_visit_id"].notna())
            ]
        )
        == 0
    )  # nosec B101
    assert len(df_meds) == 13665  # nosec B101

    return df_meds, variable_labels
