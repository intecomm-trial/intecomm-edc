import pandas as pd
from django.contrib.sites.models import Site
from django_pandas.io import read_frame

from intecomm_screening.models import PatientLog


def get_patientlog_df() -> pd.DataFrame:

    qs_patientlog = PatientLog.objects.values(
        *["patient_log_identifier", "conditions__name"]
    ).all()

    df_conditions = read_frame(qs_patientlog)
    df_conditions["hiv"] = df_conditions["conditions__name"].apply(
        lambda x: 1 if x == "HIV" else 0
    )
    df_conditions["htn"] = df_conditions["conditions__name"].apply(
        lambda x: 1 if x == "htn" else 0
    )
    df_conditions["dm"] = df_conditions["conditions__name"].apply(
        lambda x: 1 if x == "dm" else 0
    )
    df_conditions = df_conditions.pivot_table(
        index="patient_log_identifier", values=["hiv", "htn", "dm"], aggfunc="sum"
    )
    columns = [
        "site",
        "gender",
        "age_in_years",
        "patient_log_identifier",
        "screening_identifier",
        "subject_identifier",
        "group_identifier",
        "stable",
        "willing_to_screen",
        "screening_refusal_reason",
        "screening_refusal_reason_other",
    ]
    qs_patientlog = PatientLog.objects.values(*columns).all()
    df = read_frame(qs_patientlog)
    sites = {obj.name.title(): obj.id for obj in Site.objects.all()}
    df["site_id"] = df["site"].map(sites)

    df = df.merge(df_conditions, on="patient_log_identifier", how="left", suffixes=("", "_y"))

    # convert datetimes to date
    date_cols = list(df.select_dtypes(include=["datetime64", "datetime64[ns, UTC]"]).columns)
    for col in date_cols:
        df[col] = df[col].dt.normalize()

    return df
