import pandas as pd


def get_all_scheduled(df: pd.DataFrame) -> pd.DataFrame:
    df_tmp = (
        df.groupby(by=["assignment", "appt_reason"])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "visit_count"})
    )
    df_tmp1 = (
        df.groupby(by=["assignment", "appt_reason"])
        .subject_identifier.nunique()
        .to_frame()
        .reset_index()
        .rename(columns={"subject_identifier": "subjects"})
    )
    df_tmp = df_tmp.merge(df_tmp1, on=["assignment", "appt_reason"], how="left")
    df_tmp = df_tmp.merge(
        df.groupby(by=["assignment"])
        .subject_identifier.nunique()
        .to_frame()
        .rename(columns={"subject_identifier": "total_subjects"}),
        on=["assignment"],
        how="left",
    )
    df_tmp["total_visits"] = df_tmp.groupby("assignment")["visit_count"].transform("sum")
    return df_tmp
