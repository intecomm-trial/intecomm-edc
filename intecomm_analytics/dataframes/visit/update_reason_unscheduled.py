import pandas as pd

mappings = {
    "blood pressure follow up": "bp_check",
    "came sugar checkup": "glucose_check",
    "elevated glucose": "glucose_check",
    "escorted other patient": "escorted_other_patient",
    "follow up and drug refill": "study_followup_and_drug_refill",
    "for investigations": "study_followup_and_drug_refill",
    "high blood pressure": "bp_check",
    "lost his drugs.": "drug_refill",
    "missed a community visit": "study_followup_and_drug_refill",
    "missed community visit": "study_followup_and_drug_refill",
    "patient called in": "study_followup_and_drug_refill",
    "patient referral back to": "study_followup_after_referral",
    "routine (study visit)": "study_followup_and_drug_refill",
    "study & drug refill": "study_followup_and_drug_refill",
    "study & refill": "study_followup_and_drug_refill",
    "study &refil": "study_followup_and_drug_refill",
    "study visit": "study_followup_and_drug_refill",
    "study visit & drug refill": "study_followup_and_drug_refill",
}


def update_reason_unscheduled(df_all_visits: pd.DataFrame):
    df_all_visits["reason_unscheduled"] = df_all_visits["reason_unscheduled"].str.lower()
    df_all_visits["reason_unscheduled_other"] = df_all_visits[
        "reason_unscheduled_other"
    ].str.lower()
    # reasons = (
    #     df_all_visits.reason_unscheduled_other.value_counts()
    #     .to_frame()
    #     .sort_values("reason_unscheduled_other")
    #     .reset_index()
    #     .reason_unscheduled_other.to_list()
    # )
    df_all_visits["reason_unscheduled_other"] = df_all_visits[
        "reason_unscheduled_other"
    ].replace(mappings)
    df_all_visits.loc[
        df_all_visits["reason_unscheduled_other"].str.strip() == "", "reason_unscheduled_other"
    ] = pd.NA
    df_all_visits.loc[df_all_visits["reason_unscheduled"] == "other", "reason_unscheduled"] = (
        df_all_visits["reason_unscheduled_other"].str.lower()
    )
    return df_all_visits
