import pandas as pd


def get_all_unscheduled(df: pd.DataFrame) -> pd.DataFrame:
    """Number of participants who visited the facility
    unscheduled one or more times for any reason

    Note: for comm, any subject who presents to the facility
    is presenting unscheduled (using location_direction instead
    of appt_reason)
    """
    df_tmp_b = (
        df.query("appt_reason=='unscheduled' and assignment=='b'")
        .groupby(by=["assignment"])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "visit_count"})
    )
    df_tmp_b1 = (
        df.query("appt_reason=='unscheduled' and assignment=='b'")
        .groupby(by=["assignment"])
        .subject_identifier.nunique()
        .to_frame()
        .reset_index()
        .rename(columns={"subject_identifier": "subjects"})
    )
    df_tmp_b = df_tmp_b.merge(df_tmp_b1, on=["assignment"], how="left")

    df_tmp_a = (
        df.query("location_direction=='a->b' and assignment=='a'")
        .groupby(by=["assignment"])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "visit_count"})
    )
    df_tmp_a1 = (
        df.query("location_direction=='a->b' and assignment=='a'")
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
