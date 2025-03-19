from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

from intecomm_analytics.dataframes.get_appointment_df import get_appointment_df


def get_appointment_location_qa_df() -> pd.DataFrame:
    """Returns a dataframe of 1120 visits unexpectedly
    flagged as in the community.

    All 1120 appointment are conducted in the facility regardless
    of arm.
    """
    df_appt = get_appointment_df()
    cond_1120 = df_appt.visit_code == "1120"
    cond_status = (
        (df_appt.appt_status == "done")
        | (df_appt.appt_status == "incomplete")
        | (df_appt.appt_status == "in_progress")
    )
    df = df_appt[
        cond_1120
        & cond_status
        & (df_appt.schedule_name == "comm_schedule")
        & (df_appt.appt_type == "community")
    ][["subject_identifier", "site", "visit_code", "visit_code_sequence"]]
    df = df.rename(columns={"site": "site_id"})
    return df
