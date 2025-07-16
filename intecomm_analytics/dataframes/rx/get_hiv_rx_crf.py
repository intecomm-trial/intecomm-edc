import pandas as pd
from edc_analytics.stata import get_stata_labels_from_model
from edc_pdutils.constants import SYSTEM_COLUMNS
from edc_pdutils.dataframes import get_crf

from .get_rx_first_last import get_rx_first_last

__all__ = ["get_hiv_rx_crf"]


def sort_abbreviations(regimen):
    """Sort drug abbreviations alphabetically"""
    drugs = regimen.split(" + ")
    drugs.sort()
    return ",".join(drugs)


def get_hiv_rx_crf():
    mapping = {
        "DARUNAVIR/ROTINAVIR/DTG/COTRIM": "DRV + RTV + DTG + CTX",
        "DRV,RTV,DTG,CTX": "DRV + RTV + DTG + CTX",
        "DRV/RTV/DTG": "DRV + RTV + DTG",
        "TRU+ATVr": "TRU + ATVr",
        "Other first line": "firstline/unknown",
        "Other second line": "secondline/unknown",
        "Second line treatment": "secondline/unknown",
        "Other second line druga": "secondline/unknown",
        "Not refilled today": pd.NA,
    }
    df_crf = (
        get_crf(
            "intecomm_subject.drugrefillhiv",
            subject_visit_model="intecomm_subject.subjectvisit",
            read_verbose=True,
            drop_sys_columns=False,
            drop_action_item_columns=False,
        )
        .sort_values(["subject_identifier", "visit_code"])
        .reset_index(drop=True)
    )
    df_crf.loc[df_crf["rx"] == "Other, specify", "rx"] = df_crf["rx_other"]
    df_crf["rx"] = df_crf.rx.replace(mapping)

    df_crf["rx"] = df_crf["rx"].astype(str)
    df_crf["rx"] = df_crf["rx"].apply(sort_abbreviations)

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

    df_crf["crf_drugrefillhiv"] = 1

    old = [col for col in df_crf.columns if col.startswith("rx")]
    new = ["hiv_" + col for col in df_crf.columns if col.startswith("rx")]

    df_crf = (
        df_crf.rename(columns=dict(zip(old, new)))
        .rename(
            columns={
                "modifications": "hiv_rx_modifications",
                "modifications_other": "hiv_rx_modifications_other",
                "modifications_reason": "hiv_rx_modifications_reason",
                "modifications_reason_other": "hiv_rx_modifications_reason_other",
                "report_datetime": "hiv_rx_report_datetime",
            }
        )
        .drop(columns=SYSTEM_COLUMNS)
        .drop(
            columns=["consent_model", "consent_version", "crf_status", "crf_status_comments"]
        )
        .reset_index(drop=True)
    )
    return df_crf


def get_hiv_rx_variable_labels(df: pd.DataFrame) -> dict[str:str]:
    variable_labels = {}
    suffix = "hiv"
    variable_labels.update(
        **get_stata_labels_from_model(df, "intecomm_subject.drugrefillhiv", suffix)
    )
    variable_labels.update(
        {
            f"{suffix}_rx": "HIV regimens",
            f"{suffix}_rx_changed": (
                "True if change between first and last rx, not considering interim reports"
            ),
            f"{suffix}_rx_first": f"First reported {suffix} medication",
            f"{suffix}_rx_last": f"Last reported {suffix} medication",
            f"{suffix}_rx_suppl": f"Supplemental meds reported on {suffix} medication report",
            f"{suffix}_rx_concomitant": (
                f"Concomitant meds reported on {suffix} medication report"
            ),
        }
    )
    return variable_labels
