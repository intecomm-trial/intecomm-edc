import pandas as pd


def get_referrals(df: pd.DataFrame) -> pd.DataFrame:
    """Number of participants who visited the facility unscheduled
    by referral or self-referral.
    """
    df_tmp_b = (
        df.query(
            "appt_reason=='unscheduled' and assignment=='b' and "
            "reason_unscheduled=='patient_unwell_outpatient'"
        )
        .groupby(by=["assignment"])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "visit_count"})
    )
    df_tmp_b1 = (
        df.query(
            "appt_reason=='unscheduled' and assignment=='b' and "
            "reason_unscheduled=='patient_unwell_outpatient'"
        )
        .groupby(by=["assignment"])
        .subject_identifier.nunique()
        .to_frame()
        .reset_index()
        .rename(columns={"subject_identifier": "subjects"})
    )
    df_tmp_b = df_tmp_b.merge(df_tmp_b1, on=["assignment"], how="left")

    cond = (
        "location_direction=='a->b' and assignment=='a' and "
        "(location_comment.isin(['self_referral', 'referral']) "
        "or reason_unscheduled=='patient_unwell_outpatient')"
    )
    df_tmp_a = (
        df.query(cond)
        .groupby(by=["assignment"])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "visit_count"})
    )
    df_tmp_a1 = (
        df.query(cond)
        .groupby(by=["assignment"])
        .subject_identifier.nunique()
        .to_frame()
        .reset_index()
        .rename(columns={"subject_identifier": "subjects"})
    )
    df_tmp_a = df_tmp_a.merge(df_tmp_a1, on=["assignment"], how="left")

    df_tmp = pd.concat([df_tmp_a, df_tmp_b], ignore_index=True)
    df_tmp = df_tmp.merge(
        df.groupby(by=["assignment"])
        .subject_identifier.nunique()
        .to_frame()
        .rename(columns={"subject_identifier": "total_subjects"}),
        on=["assignment"],
        how="left",
    )
    df_tmp["prop_subjects"] = df_tmp.subjects / df_tmp.total_subjects
    return df_tmp
