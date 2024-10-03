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

    sites = {obj.domain: obj.id for obj in Site.objects.all()}
    df["site_id"] = df["site"].map(sites)

    # replace
    df = df.replace({"Not Applicable: e.g. male or post-menopausal": "N/A"})
    df = df.replace({"Not applicable": "N/A"})
    df = df.replace({True: 1})
    df = df.replace({False: 0})

    # convert to datetime
    cols = ["report_datetime", "created"]
    df[cols] = df[cols].apply(pd.to_datetime)

    # convert datetimes to date
    date_cols = list(df.select_dtypes(include=["datetime64", "datetime64[ns, UTC]"]).columns)
    df = normalize_date_columns(df, cols=date_cols)
    df["dob"] = pd.to_datetime(df["dob"])
    df["age_in_years"] = (
        pd.to_datetime(df["report_datetime"].dt.date).dt.year - df["dob"].dt.year
    )
    return df
