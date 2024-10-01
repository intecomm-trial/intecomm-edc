import pandas as pd

from ..constants import DM_HTN, DM_ONLY, HIV_DM, HIV_DM_HTN, HIV_HTN, HIV_ONLY, HTN_ONLY


def get_conditions_by_gender(df: pd.DataFrame, summarize: bool | None = None) -> pd.DataFrame:
    """Given a dataframe calculates a freq table for each condition
    by gender.

    For example:

        # with patient log
        patientlog_df = get_patientlog_df()
        df = get_conditions_by_gender(patientlog_df, summarize=True)

        # with diagnoses table
        dx_df = get_diagnoses_df()
        df = get_conditions_by_gender(dx_df, summarize=True)

    """

    s = df[(df["hiv"] == 1) & (df["htn"] == 0) & (df["dm"] == 0)]["gender"].value_counts()
    df1 = s.to_frame().reset_index()
    df1["label"] = HIV_ONLY
    cond_df = df1.copy()

    for hiv, htn, dm, label in [
        (0, 1, 0, HTN_ONLY),
        (0, 0, 1, DM_ONLY),
        (1, 0, 1, HIV_DM),
        (1, 1, 0, HIV_HTN),
        (1, 1, 1, HIV_DM_HTN),
        (0, 1, 1, DM_HTN),
    ]:
        s = df[(df["hiv"] == hiv) & (df["htn"] == htn) & (df["dm"] == dm)][
            "gender"
        ].value_counts()
        df1 = s.to_frame().reset_index()
        df1["label"] = label
        cond_df = pd.concat([cond_df, df1])
    cond_df = cond_df.reset_index(drop=True)
    if summarize:
        cond_df = cond_df.pivot(index="label", columns=["gender"], values=["count"])
        cond_df.columns = [col[1] for col in cond_df.columns]
        cond_df = cond_df.reset_index()
        cond_df["Total"] = cond_df["Female"] + cond_df["Male"]
        cond_df.loc[len(cond_df)] = {
            "label": "Total",
            "Female": cond_df["Female"].sum(),
            "Male": cond_df["Male"].sum(),
            "Total": cond_df["Total"].sum(),
        }
        cond_df["F_PROP"] = cond_df["Female"] / cond_df.loc[7]["Female"]
        cond_df["M_PROP"] = cond_df["Male"] / cond_df.loc[7]["Male"]
        cond_df["T_PROP"] = cond_df["Total"] / cond_df.loc[7]["Total"]
    return cond_df
