import pandas as pd
from edc_pdutils.dataframes import get_crf

from .prepare_rx_columns import prepare_rx_columns

__all__ = ["get_dm_rx_crf"]


def get_dm_rx_crf(suffix: str) -> pd.DataFrame:
    model = "intecomm_subject.drugrefilldm"
    _, model_name = model.split(".")
    mappings = {
        "tilypltin": "teneligliptin",
        "tliyptin": "teneligliptin",
        "tilyptin": "teneligliptin",
        "aspirin": "aspirin_concomitant",
        "glucovan": "metformin,glyburide",
        "ilet 1": "metformin,glimepiride",
        "tenegliptin": "teneligliptin",
        "neuroton": "neuroton_suppl",
        "ecorin": "aspirin_concomitant",
        "life style": "life_style",
        "tenegliptine": "teneligliptin",
        "lifestyle management": "life_style",
        "lifestyle": "life_style",
        "neuro support": "neurosupport_suppl",
        "ilet b1": "metformin,glimepiride",
        "gamma 2t": "gabapentin",
        "neurotone": "neurotone_suppl",
        "vitamin b complex": "vitamin_b_complex_suppl",
        "meloxicam": "meloxicam_suppl",
        "neurosupport": "neurosupport_suppl",
        "gabapentic": "gabapentin",
        "tilynegliptin": "teneligliptin",
        "dapsin": "dapsone_concomitant",
        "not on medication": "life_style",
        "vildagliptin": "vildagliptin",
        "ablept": "gabapentin",
        "patient is on lifestyle": "life_style",
        "dapzin": "dapsone_concomitant",
        "metagliptin": "metformin,glipizide",
        "gabapentine": "gabapentin",
    }
    df_crf = (
        get_crf(
            model,
            subject_visit_model="intecomm_subject.subjectvisit",
            read_verbose=False,
            drop_sys_columns=False,
            drop_action_item_columns=False,
        )
        .sort_values(["subject_identifier", "visit_code"])
        .reset_index(drop=True)
    )

    df_crf = prepare_rx_columns(df_crf, suffix, mappings, model_name)
    return df_crf
