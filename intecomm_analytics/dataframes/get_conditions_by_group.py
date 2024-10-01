import pandas as pd

from ..constants import DM_HTN, DM_ONLY, HIV_DM, HIV_DM_HTN, HIV_HTN, HIV_ONLY, HTN_ONLY


def cond_value_counts(source_df: pd.DataFrame, hiv: int, htn: int, dm: int) -> pd.Series:
    return source_df[
        (source_df["hiv"] == hiv) & (source_df["htn"] == htn) & (source_df["dm"] == dm)
    ]["country"].value_counts()


def get_conditions_by_country(
    source_df: pd.DataFrame, summarize: bool | None = None
) -> pd.DataFrame:
    """Given a dataframe calculates a freq table for each condition
    by country.

    For example:

        # with patient log
        patientlog_df = get_patientlog_df()
        df = get_conditions_by_country(patientlog_df, summarize=True)

        # with diagnoses table
        dx_df = get_diagnoses_df()
        df = get_conditions_by_country(dx_df, summarize=True)

    """
    df = pd.DataFrame()
    for index, data in enumerate(
        [
            (1, 0, 0, HIV_ONLY),
            (0, 1, 0, HTN_ONLY),
            (0, 0, 1, DM_ONLY),
            (1, 0, 1, HIV_DM),
            (1, 1, 0, HIV_HTN),
            (1, 1, 1, HIV_DM_HTN),
            (0, 1, 1, DM_HTN),
        ]
    ):
        hiv, htn, dm, label = data
        df1 = cond_value_counts(source_df, hiv, htn, dm).to_frame().reset_index()
        df1["label"] = label
        df = pd.concat([df, df1])
    df = df.reset_index(drop=True)
    if summarize:
        df = df.pivot(index="label", columns=["country"], values=["count"])
        df.columns = [col[1] for col in df.columns]
        df = df.reset_index()
        df["total"] = df["uganda"] + df["tanzania"]
        df.loc[len(df)] = {
            "label": "total",
            "uganda": df["uganda"].sum(),
            "tanzania": df["tanzania"].sum(),
            "total": df["total"].sum(),
        }
        # column props
        df["ug_cprop"] = df["uganda"] / df.loc[7]["uganda"]
        df["tz_cprop"] = df["tanzania"] / df.loc[7]["tanzania"]
        df["t_cprop"] = (df["uganda"] + df["tanzania"]) / df.loc[7]["total"]
        # row prop
        df["ug_rprop"] = df["uganda"] / df["total"]
        df["tz_rprop"] = df["tanzania"] / df["total"]
        df["t_rprop"] = df["ug_rprop"] + df["tz_rprop"]
    return df
