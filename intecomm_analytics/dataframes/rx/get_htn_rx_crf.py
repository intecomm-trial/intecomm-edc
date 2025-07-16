import pandas as pd
from edc_analytics.stata import get_stata_labels_from_model
from edc_pdutils.dataframes import get_crf

from .prepare_rx_columns import prepare_rx_columns

__all__ = ["get_htn_rx_crf"]


def get_htn_rx_crf(suffix: str) -> pd.DataFrame:
    model = "intecomm_subject.drugrefillhtn"
    _, model_name = model.split(".")
    df_crf = (
        get_crf(
            "intecomm_subject.drugrefillhtn",
            subject_visit_model="intecomm_subject.subjectvisit",
            read_verbose=False,
            drop_sys_columns=False,
            drop_action_item_columns=False,
        )
        .sort_values(["subject_identifier", "visit_code"])
        .reset_index(drop=True)
    )

    mappings = {
        "telmistan hydrochlorothiazide": "telmisartan_h",
        "telmisartan.h": "telmisartan_h",
        "telvas-h 40": "telmisartan_h",
        "telvas h": "telmisartan_h",
        "telvas-h": "telmisartan_h",
        "vitamin bcomplex": "vitamin_bcomplex_suppl",
        "spirin": "aspirin_concomitant",
        "junior_aspirin": "aspirin_concomitant",
        "aspirin": "aspirin_concomitant",
        "pregabalin, calcivita": "pregabalin,calcivita_suppl",
        "pregabalin, neuroton": "pregabalin,neuroton_suppl",
        "pregabalin  glucosame": "pregabalin,glucosame_suppl",
        "pre gabaline, glucosame": "pregabalin,glucosame_suppl",
        "pre gabaline": "pregabalin",
        "pre gabalin, nat b": "pregabalin,nat_b_suppl",
        "on non pharmacological treatment": "nonpharmacological_treatment",
        "non pharmacological means": "nonpharmacological_treatment",
        "olmart 40-h": "olmesartan_h",
        "nibivolol chlorhydrate": "nibivolol_chlorhydrate",
        "neurotone": "neuroton_e_suppl",
        "neuroton": "neuroton_suppl",
        "neurobion": "neurobion_suppl",
        "neurobin": "neurobion_suppl",
        "neurosupport": "neurosupport_suppl",
        "neurostrong": "neurostrong_suppl",
        "nat b": "nat_b_suppl",
        "monteluckast, isosebide mononitrate": (
            "monteluckast_concomitant,isosebide_mononitrate"
        ),
        "liver cool": "livercool_concomitant",
        "life style": "life_style",
        "isosorbide mononitrate, nat b": "isosebide_mononitrate,nat_b_suppl",
        "isosobide mono nitrate": "isosebide_mononitrate",
        "isosobide dinitrate": "isosebide_dinitrate",
        "isosibide mononitrate": "isosebide_mononitrate",
        "isoborbide denitrate,  sodium valporate": (
            "isosebide_dinitrate,sodium_valporate_concomitant"
        ),
        "isosobidemononitrate": "isosebide_mononitrate",
        "isosobide mononitrate": "isosebide_mononitrate",
        "ismn isosobide mononitrate": "isosebide_mononitrate",
        "ismn": "isosebide_mononitrate",
        "gizland": "irbesartan,amlodipine",
        "fluxetine": "fluxetine_concomitant",
        "ecorine": "aspirin_concomitant",
        "ecorin": "aspirin_concomitant",
        "digoxine": "digoxine",
        "drugs stopped": "drugs_stopped",
        "clindipine, nerozinc": "clindipine,nerozinc_suppl",
        "asomex": "amlodipine",
        "arbitel": "telmisartan",
        "aprinox": "bendroflumethiazide",
        "abitel h": "telmisartan_h",
        "abetil-h": "telmisartan_h",
        "added some drug": "added_unknown_concomitant",
    }
    df_crf = prepare_rx_columns(df_crf, suffix, mappings, model_name)
    return df_crf


def get_htn_rx_variable_labels(df):
    variable_labels = {}
    suffix = "htn"
    variable_labels.update(
        **get_stata_labels_from_model(df, "intecomm_subject.drugrefillhtn", suffix)
    )
    variable_labels.update(
        {
            f"{suffix}_rx": "HTN medications",
            f"{suffix}_rx_changed": (
                "True if change between first and last rx, not considering interim reports"
            ),
            f"{suffix}_rx_first": f"First reported {suffix} medication",
            f"{suffix}_rx_last": f"Last reported {suffix} medication",
            f"{suffix}_rx_suppl": f"Supplemental meds reported on {suffix} medication report",
            f"{suffix}_rx_concomitant": (
                f"Concomitant meds reported on {suffix} medication report"
            ),
            f"{suffix}_rx_days": (
                f"Days prescribed counting from day of {suffix} medication report"
            ),
        }
    )
    return variable_labels
