import pandas as pd


def get_drug_refills_unscheduled(df: pd.DataFrame) -> pd.DataFrame:
    """Number of community participants who visited the
    facility to pick up medicines
    """
    cond = (
        "location_direction=='a->b' and assignment=='a' and "
        "(location_comment.isin(['drug_refill']) or reason_unscheduled.isin(['drug_refill']))"
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
    df_tmp = df_tmp_a.merge(df_tmp_a1, on=["assignment"], how="left")

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
