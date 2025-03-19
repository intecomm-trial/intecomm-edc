import pandas as pd

from intecomm_analytics.dataframes import get_patientlog_df


def get_screening_diagnoses_df() -> pd.DataFrame:
    df = get_patientlog_df()
    df_dx = df.groupby(["hiv", "htn", "dm"]).size().to_frame()
    df_dx = df_dx.reset_index(drop=True)
    return df_dx
