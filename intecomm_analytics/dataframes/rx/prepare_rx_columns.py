import pandas as pd
from edc_pdutils.constants import SYSTEM_COLUMNS

from .get_rx_first_last import get_rx_first_last


def prepare_rx_columns(
    df_crf: pd.DataFrame, suffix: str, mappings: dict[str, str], model_name: str
) -> pd.DataFrame:
    """Run following getting df from drugrefillhtn, drugrefilldm.

    See get_dm_rx_crf, get_htn_rx_crf
    """
    df_crf["rx_other"] = df_crf["rx_other"].str.lower()
    df_crf["rx_other"] = df_crf["rx_other"].replace(mappings)
    df_crf["rx"] = df_crf["rx"].str.replace("OTHER", "", case=False)
    df_crf["rx"] = df_crf["rx"].str.strip(", ").str.replace(r",+", ",", regex=True)

    df_crf["rx_concomitant"] = pd.NA
    df_crf["rx_concomitant"] = df_crf["rx_other"].str.extract(r"(\b\w+_concomitant\b)")
    df_crf["rx_other"] = df_crf["rx_other"].str.replace(
        r"\b\w+_concomitant\b,?", "", regex=True
    )
    df_crf["rx_other"] = df_crf["rx_other"].str.strip(", ").str.replace(r",+", ",", regex=True)

    df_crf["rx_supplement"] = pd.NA
    df_crf["rx_supplement"] = df_crf["rx_other"].str.extract(r"(\b\w+_suppl\b)")
    df_crf["rx_other"] = df_crf["rx_other"].str.replace(r"\b\w+_suppl\b,?", "", regex=True)
    df_crf["rx_other"] = df_crf["rx_other"].str.strip(", ").str.replace(r",+", ",", regex=True)

    df_crf.loc[df_crf["rx_other"].str.strip() == "", "rx_other"] = pd.NA
    df_crf.loc[df_crf["rx_other"].notna(), "rx"] = (
        df_crf["rx"].fillna("").str.lower() + "," + df_crf["rx_other"].str.lower()
    )
    df_crf.loc[df_crf["rx"].str.contains("junior_aspirin"), "rx_concomitant"] = (
        df_crf["rx_concomitant"].fillna("") + ",aspirin_concomitant"
    )
    df_crf["rx"] = df_crf["rx"].str.replace(r"junior_aspirin", "", regex=False)
    df_crf.loc[df_crf["rx"].str.contains("aspirin"), "rx_concomitant"] = (
        df_crf["rx_concomitant"].fillna("") + ",aspirin_concomitant"
    )
    df_crf["rx"] = df_crf["rx"].str.replace("aspirin", "", regex=False)

    df_crf.loc[df_crf["rx"].str.contains("vitamin_b_folic_acid"), "rx_concomitant"] = (
        df_crf["rx_concomitant"].fillna("") + ",vitamin_bcomplex_concomitant"
    )
    df_crf["rx"] = df_crf["rx"].str.replace("vitamin_b_folic_acid", "", regex=False)

    df_crf["rx"] = df_crf["rx"].str.strip(", ").str.replace(r",+", ",", regex=True)

    df_crf["rx_concomitant"] = (
        df_crf["rx_concomitant"].str.strip(", ").str.replace(r",+", ",", regex=True)
    )

    df_first_last = get_rx_first_last(df_crf)

    df_crf = df_crf.merge(
        df_first_last[["subject_identifier", "rx_first", "rx_last", "rx_changed"]],
        on="subject_identifier",
        how="left",
    )
    df_crf["rx_changed"] = 0
    df_crf.loc[
        (df_crf["rx_first"].notna())
        & (df_crf["rx_last"].notna())
        & (df_crf["rx_first"] != df_crf["rx_last"])
        & (df_crf["rx_first"] != "Other, specify"),
        "rx_changed",
    ] = 1

    df_crf[f"crf_{model_name}"] = 1

    old = [col for col in df_crf.columns if col.startswith("rx")]
    new = [f"{suffix}_" + col for col in df_crf.columns if col.startswith("rx")]
    df_crf = df_crf.rename(columns=dict(zip(old, new))).reset_index(drop=True)

    old = [col for col in df_crf.columns if col.endswith(f"_{suffix}")]
    new = [
        col[: -1 * (len(suffix) + 1)] for col in df_crf.columns if col.endswith(f"_{suffix}")
    ]
    df_crf = df_crf.rename(columns=dict(zip(old, new)))
    df_crf = df_crf.rename(
        columns={
            "modifications": f"{suffix}_rx_modifications",
            "modifications_other": f"{suffix}_rx_modifications_other",
            "modifications_reason": f"{suffix}_rx_modifications_reason",
            "modifications_reason_other": f"{suffix}_rx_modifications_reason_other",
        }
    )
    df_crf = df_crf.drop(columns=SYSTEM_COLUMNS)
    df_crf = df_crf.drop(
        columns=["consent_model", "consent_version", "crf_status", "crf_status_comments"]
    )
    df_crf = df_crf.rename(columns={"report_datetime": f"{suffix}_rx_report_datetime"})
    return df_crf
