import pandas as pd


def get_subjects_who_missed_scheduled(df: pd.DataFrame) -> pd.DataFrame:
    """Number of participants who missed one or more appointments"""
    df_tmp = (
        df.query("appt_reason=='scheduled' and appt_timing=='missed'")
        .groupby(by=["assignment"])
        .subject_identifier.nunique()
        .to_frame()
        .reset_index()
        .rename(columns={"subject_identifier": "freq"})
    )
    df_tmp1 = (
        df.query("appt_reason=='scheduled'")
        .groupby(by=["assignment"])
        .subject_identifier.nunique()
        .to_frame()
        .reset_index()
        .rename(columns={"subject_identifier": "freq"})
    )
    df_tmp = df_tmp.merge(df_tmp1, on=["assignment"], how="left", suffixes=["", "_y"]).rename(
        columns={"freq_y": "total"}
    )
    df_tmp["prop"] = df_tmp.freq / df_tmp.total
    return df_tmp
