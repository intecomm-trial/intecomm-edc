import pandas as pd
from edc_appointment.analytics import get_appointment_df
from edc_appointment.constants import CANCELLED_APPT, SKIPPED_APPT
from edc_constants.constants import NOT_APPLICABLE
from edc_model_to_dataframe.constants import SYSTEM_COLUMNS
from edc_pdutils.dataframes import get_subject_visit
from edc_pdutils.dataframes.get_subject_visit import convert_visit_code_to_float

from ..get_location_update import get_location_update
from ..visit import get_subject_visit_missed, update_reason_unscheduled


def get_appt_df(df_main_1858: pd.DataFrame | None = None) -> pd.DataFrame:
    # using df_appt
    # get all appointments and merge in missed reasons,
    # unscheduled reasons, and location update (direction, location_comment)
    # the freq per cohort should match df_main_1858

    if not isinstance(df_main_1858, pd.DataFrame):
        from ..df_main_1858 import get_df_main_1858

        df_main_1858 = get_df_main_1858(None, fasting_hours=8.0)

    assert len(df_main_1858) == 1858  # nosec B101
    df_appt = (
        get_appointment_df()
        .merge(
            df_main_1858[
                [
                    "subject_identifier",
                    "group_identifier",
                    "assignment",
                    "gender",
                    "country",
                    "primary_cohort",
                    "primary_cohort_str",
                    "htn",
                    "hiv",
                    "dm",
                    "weight",
                    "bmi",
                ]
            ],
            on="subject_identifier",
            how="left",
        )
        .drop(columns=SYSTEM_COLUMNS)
        .sort_values(by=["subject_identifier", "appt_datetime"])
        .reset_index(drop=True)
    )
    df_appt = (
        df_appt[df_appt.subject_identifier.isin(df_main_1858.subject_identifier)]
        .copy()
        .reset_index(drop=True)
    )

    assert len(df_appt) == 24229  # nosec B101
    assert len(df_appt.subject_identifier.unique()) == 1858  # nosec B101

    df_visit = get_subject_visit("intecomm_subject.subjectvisit")
    df_visit = (
        df_visit[df_visit.subject_identifier.isin(df_main_1858.subject_identifier)]
        .copy()
        .reset_index(drop=True)
    )

    assert len(df_visit) == 20795  # nosec B101

    df_visit = update_reason_unscheduled(df_visit)

    df_subjectvisitmissed = get_subject_visit_missed().rename(
        columns={"missed_reasons": "reason_missed_detail"}
    )
    df_visit = df_visit.merge(
        df_subjectvisitmissed[["subject_visit_id", "reason_missed_detail"]],
        on="subject_visit_id",
        how="left",
    )
    df_location_update = get_location_update(None).rename(
        columns={"direction": "location_direction"}
    )
    df_visit = df_visit.merge(
        df_location_update[["subject_visit_id", "location_direction", "location_comment"]],
        how="left",
        on=["subject_visit_id"],
    )
    assert len(df_visit) == 20795  # nosec B101

    df_appt["visit_code_str"] = df_appt["visit_code"]
    convert_visit_code_to_float(df_appt)

    df_appt = df_appt.merge(
        df_visit[
            [
                "appointment_id",
                "subject_visit_id",
                "location_direction",
                "location_comment",
                "reason_missed_detail",
                "reason_unscheduled",
            ]
        ],
        on=["appointment_id"],
        how="left",
    )

    assert len(df_appt) == 24229  # nosec B101
    assert len(df_appt[df_appt.subject_visit_id.notna()]) == 20795  # nosec B101

    df_appt.loc[df_appt.reason_unscheduled == NOT_APPLICABLE.lower(), "reason_unscheduled"] = (
        pd.NA
    )
    df_appt.loc[df_appt.reason_missed_detail.isna(), "reason_missed_detail"] = pd.NA
    df_appt.loc[df_appt.location_direction.isna(), "location_direction"] = pd.NA
    df_appt.loc[df_appt.comment.isna(), "comment"] = pd.NA
    df_appt.loc[df_appt.comment.str.strip().isin(["", "None"]), "comment"] = pd.NA
    df_appt.loc[df_appt.location_comment.str.strip() == "", "location_comment"] = pd.NA
    df_appt.loc[
        (df_appt.assignment == "a") & (df_appt.location_comment.isna()), "location_comment"
    ] = "unknown"
    df_appt.loc[
        (df_appt.location_direction == "a->b")
        & (df_appt.reason_unscheduled == "patient_unwell_outpatient")
        & (df_appt.location_comment.isna()),
        "location_comment",
    ] = "referral"
    df_appt.loc[
        df_appt.location_comment.isin(["self_referral", "referral"])
        & (df_appt.assignment == "a"),
        "reason_unscheduled",
    ] = "patient_unwell_outpatient"

    df_appt = df_appt.rename(columns={"comment": "appt_comment"})

    # df_appt = df_appt[
    #     (df_appt.primary_cohort_str != "UNDEFINED")
    #     & ~(df_appt.appt_status.isin([CANCELLED_APPT, SKIPPED_APPT]))
    # ].reset_index(drop=True)

    df_appt = df_appt[~(df_appt.appt_status.isin([CANCELLED_APPT, SKIPPED_APPT]))].reset_index(
        drop=True
    )

    assert len(df_appt) == 20953  # nosec B101

    assert len(df_appt[df_appt.subject_visit_id.notna()]) == 20785  # nosec B101

    assert df_appt.subject_identifier.nunique() == 1858  # nosec B101

    return df_appt
