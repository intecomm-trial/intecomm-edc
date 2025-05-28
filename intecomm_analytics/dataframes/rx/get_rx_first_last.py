import pandas as pd


def get_rx_first_last(df_crf: pd.DataFrame) -> pd.DataFrame:
    df_first = (
        df_crf[["subject_identifier", "rx"]]
        .groupby("subject_identifier")
        .agg(["first"])
        .reset_index()
    )
    df_first.columns = ["subject_identifier", "rx_first"]
    df_last = (
        df_crf[["subject_identifier", "rx"]]
        .groupby("subject_identifier")
        .agg(["last"])
        .reset_index()
    )
    df_last.columns = ["subject_identifier", "rx_last"]
    df_rx = pd.merge(df_first, df_last, on="subject_identifier", how="left").reset_index()
    df_rx["rx_changed"] = 0
    df_rx.loc[
        (df_rx["rx_first"] != df_rx["rx_last"]) & (df_rx["rx_first"] != "Other, specify"),
        "rx_changed",
    ] = 1
    return df_rx.reset_index(drop=True)
