import pandas as pd


def get_scheduled_and_missed(df: pd.DataFrame) -> pd.DataFrame:
    df_tmp = (
        df.query("appt_reason=='scheduled' and appt_timing=='missed'")
        .groupby(by=["assignment"])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "freq"})
    )
    df_tmp1 = (
        df.query("appt_reason=='scheduled'")
        .groupby(by=["assignment"])
        .size()
        .to_frame()
        .reset_index()
        .rename(columns={0: "freq"})
    )
    df_tmp = df_tmp.merge(df_tmp1, on=["assignment"], how="left", suffixes=["", "_y"]).rename(
        columns={"freq_y": "total"}
    )
    df_tmp["prop"] = df_tmp.freq / df_tmp.total
    return df_tmp
