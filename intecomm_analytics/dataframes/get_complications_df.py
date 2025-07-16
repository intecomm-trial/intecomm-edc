from pathlib import Path

import pandas as pd
from edc_analytics.stata import get_stata_labels_from_model
from edc_model_to_dataframe.constants import SYSTEM_COLUMNS
from edc_pdutils.dataframes import get_crf

from intecomm_analytics.dataframes.main_1858_to_stata import df_main_variable_labels

from .appt import get_appt_df


def get_all_complications_df():
    df_baseline, variable_labels = get_complications_df(
        model="intecomm_subject.complicationsbaseline"
    )
    df_followup, variable_labels_followup = get_complications_df(
        model="intecomm_subject.complicationsfollowup"
    )
    df_complications = pd.concat([df_baseline, df_followup])
    assert (
        len(df_complications[df_complications["subject_visit_id"].duplicated(keep=False)]) == 0
    )  # nosec B101
    variable_labels.update(**variable_labels_followup)
    return df_complications, variable_labels


def get_complications_df(
    model: str, analysis_folder: Path | None = None
) -> tuple[pd.DataFrame, dict[str:str]]:
    variable_labels = {}
    _, model_name = model.split(".")
    df_complications = get_crf(
        model=model,
        subject_visit_model="intecomm_subject.subjectvisit",
        drop_sys_columns=True,
    )
    df_complications["crf"] = model_name

    df_complications = df_complications.drop(
        columns=[col for col in df_complications.columns if "_ago" in col]
    )
    sys_cols = SYSTEM_COLUMNS + ["id"]
    df_complications = df_complications.drop(
        columns=[col for col in df_complications.columns if col in sys_cols]
    )
    df_complications = df_complications.drop(
        columns=[
            col
            for col in df_complications.columns
            if col in ["consent_model", "consent_version", "crf_status", "crf_status_comments"]
        ]
    )

    # for baseline, put estimated_dates, derived from _ago, into date columns
    # followup only has date columns
    estimate_columns = [col for col in df_complications.columns if "_estimated_date" in col]
    if estimate_columns:
        complications = [
            "stroke",
            "heart_attack",
            "renal_disease",
            "vision",
            "numbness",
            "foot_ulcers",
        ]
        for prefix in complications:
            if f"{prefix}_date" not in df_complications.columns:
                df_complications[f"{prefix}_date"] = pd.NaT
            mask = (df_complications[prefix] == "Yes") & (
                df_complications[f"{prefix}_date"].isna()
            )
            df_complications.loc[mask, f"{prefix}_date"] = df_complications.loc[
                mask, f"{prefix}_estimated_date"
            ]
        df_complications = df_complications.drop(columns=estimate_columns)

    df_complications = df_complications.rename(
        columns={
            "subject_visit": "subject_visit_id",
            "report_datetime": "report_datetime_complications",
            "heart_attack": "heart_attack_complications",
            "renal_disease": "renal_disease_complications",
            "vision": "vision_complications",
            "numbness": "numbness_complications",
            "foot_ulcers": "foot_ulcers_complications",
            "stroke": "stroke_complications",
            "heart_attack_date": "heart_attack_date_complications",
            "renal_disease_date": "renal_disease_date_complications",
            "vision_date": "vision_date_complications",
            "numbness_date": "numbness_date_complications",
            "foot_ulcers_date": "foot_ulcers_date_complications",
            "stroke_date": "stroke_date_complications",
            "complications_other": "other_complications",
        }
    )
    for col in [
        "stroke_date_complications",
        "heart_attack_date_complications",
        "renal_disease_date_complications",
        "vision_date_complications",
        "numbness_date_complications",
        "foot_ulcers_date_complications",
    ]:
        df_complications[col] = df_complications[col].astype("datetime64[ns]")

    df_complications["crf_complications"] = 1

    df_complications.loc[
        df_complications["other_complications"].str.strip() == "", "other_complications"
    ] = pd.NA
    df_complications = df_complications.fillna(pd.NA)

    variable_labels.update(
        **get_stata_labels_from_model(
            df_complications, "intecomm_subject.complicationsbaseline", "complications"
        )
    )
    variable_labels.update(
        **get_stata_labels_from_model(
            df_complications, "intecomm_subject.complicationsfollowup", "complications"
        )
    )

    assert (
        len(df_complications[df_complications["subject_visit_id"].duplicated(keep=False)]) == 0
    )  # nosec B101

    if analysis_folder:
        df_appt = get_appt_df()
        df_appt = df_appt.merge(
            df_complications[
                [
                    "subject_visit_id",
                    *[
                        col
                        for col in df_complications.columns
                        if col.endswith("complications") and "estimated" not in col
                    ],
                ]
            ],
            on="subject_visit_id",
            how="left",
            suffixes=("", "_y"),
        )
        assert len(df_appt) == 20953  # nosec B101
        variable_labels.update(
            **get_stata_labels_from_model(df_appt, "edc_appointment.appointment")
        )
        variable_labels.update(**df_main_variable_labels())
        df_appt = df_appt.drop(columns=["appt_type_other", "document_status_comments"])
        df_appt["timepoint"] = df_appt["timepoint"].astype("Int64")
        df_appt["subject_visit_id"] = df_appt["subject_visit_id"].astype("str")
        df_appt["appointment_id"] = df_appt["appointment_id"].astype("str")
        df_appt.to_stata(
            path=analysis_folder / "complications.dta",
            variable_labels=variable_labels,
            version=118,
            write_index=False,
        )
    return df_complications, variable_labels
