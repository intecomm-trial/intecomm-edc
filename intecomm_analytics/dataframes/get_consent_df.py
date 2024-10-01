import pandas as pd
from django.contrib.sites.models import Site
from django_pandas.io import read_frame
from edc_analytics.utils import normalize_date_columns
from edc_model import duration_to_date

from intecomm_consent.models import SubjectConsent


def duration_to_date_by_row(row: pd.Series, col: str = None):
    return duration_to_date(duration_text=row[col], reference_date=row["report_datetime"])


def get_consent_df(df: pd.DataFrame | None = None) -> pd.DataFrame:
    df = pd.DataFrame() if not hasattr(df, "empty") else df
    if df.empty:
        exclude = [
            "identity",
            "confirm_identity",
            "initials",
            "legal_name",
            "familiar_name",
            "hospital_identifier",
            "hostname_created",
            "hostname_modified",
            "device_created",
            "device_modified",
            "locale_created",
            "locale_modified",
            "subject_identifier_aka",
            "slug",
            "subject_identifier_as_pk",
        ]
        fldnames = [
            fld.name for fld in SubjectConsent._meta.get_fields() if fld.name not in exclude
        ]
        qs_consent = SubjectConsent.objects.values(*fldnames).all()
        df = read_frame(qs_consent)

    # df["gender"] = df["gender"].apply(lambda x: "F" if x == "Female" else x)
    # df["gender"] = df["gender"].apply(lambda x: "M" if x == "Male" else x)

    sites = {obj.domain: obj.id for obj in Site.objects.all()}
    df["site_id"] = df["site"].map(sites)

    # replace
    df = df.replace({"Not Applicable: e.g. male or post-menopausal": "N/A"})
    df = df.replace({"Not applicable": "N/A"})
    df = df.replace({True: 1})
    df = df.replace({False: 0})

    # convert all to float
    # cols = [
    #     "age_in_years",
    #     "dia_blood_pressure_avg",
    #     "dia_blood_pressure_one",
    #     "dia_blood_pressure_two",
    #     "sys_blood_pressure_avg",
    #     "sys_blood_pressure_one",
    #     "sys_blood_pressure_two",
    # ]
    # df[cols] = df[cols].apply(pd.to_numeric)

    # convert to datetime
    cols = ["report_datetime", "created"]
    df[cols] = df[cols].apply(pd.to_datetime)

    # df_patientlog = read_frame(qs_patientlog)
    # df = df.merge(df_patientlog, on="screening_identifier", how="left", suffixes=("", "_y"))

    # attended baseline visit
    # qs_subjectvisit = SubjectVisit.objects.values(
    #     "appointment__subject_identifier", "report_datetime"
    # ).filter(visit_code="1000", visit_code_sequence=0)
    # df_subjectvisit = read_frame(qs_subjectvisit)
    # df_subjectvisit = df_subjectvisit.rename(
    #     columns={"appointment__subject_identifier": "subject_identifier"}
    # )
    # df = df.merge(df_subjectvisit, on="subject_identifier", how="left", suffixes=("", "_y"))

    # convert datetimes to date
    date_cols = list(df.select_dtypes(include=["datetime64", "datetime64[ns, UTC]"]).columns)
    df = normalize_date_columns(df, cols=date_cols)
    df["dob"] = pd.to_datetime(df["dob"])
    df["age_in_years"] = (
        pd.to_datetime(df["report_datetime"].dt.date).dt.year - df["dob"].dt.year
    )
    return df
