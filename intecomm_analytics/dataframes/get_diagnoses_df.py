import pandas as pd
from django.contrib.sites.models import Site
from django_pandas.io import read_frame
from edc_constants.constants import OTHER
from edc_sites.site import sites

from intecomm_consent.models import SubjectConsent
from intecomm_lists.list_data import list_data
from intecomm_prn.models import EndOfStudy
from intecomm_reports.models import Diagnoses
from intecomm_screening.models import PatientLog


def get_diagnoses_df() -> pd.DataFrame:

    df = read_frame(Diagnoses.objects.all())
    df["site_id"] = df["site"].map({obj.domain: obj.id for obj in Site.objects.all()})
    df = df.drop(columns=["site"])
    df = df.reset_index(drop=True)

    # add group identifier
    qs_patientlog = PatientLog.objects.values("subject_identifier", "group_identifier").all()
    df_pat = read_frame(qs_patientlog)
    df = df.merge(df_pat, on="subject_identifier", how="left")

    # add demographics from consent
    df_consent = read_frame(
        SubjectConsent.objects.values("subject_identifier", "gender", "dob", "site").all()
    )
    df_consent["site_id"] = df_consent["site"].map(
        {obj.domain: obj.id for obj in Site.objects.all()}
    )
    df_consent = df_consent.drop(columns=["site"])
    df_consent = df_consent.reset_index(drop=True)

    df = df.merge(
        df_consent[["subject_identifier", "gender", "dob", "site_id"]],
        how="left",
        on=["subject_identifier", "site_id"],
    )

    df_eos = read_frame(
        EndOfStudy.objects.values(
            "subject_identifier",
            "offstudy_datetime",
            "offstudy_reason",
            "other_offstudy_reason",
            "site",
        ).all()
    )
    df_eos["site_id"] = df_eos["site"].map({obj.domain: obj.id for obj in Site.objects.all()})
    offstudy_reasons = {k: v for k, v in list_data.get("intecomm_lists.offstudyreasons")}

    df_eos["offstudy_reason"] = df_eos.apply(
        lambda row: (
            row["other_offstudy_reason"]
            if row["offstudy_reason"] == offstudy_reasons.get(OTHER)
            else row["offstudy_reason"]
        ),
        axis=1,
    )

    # recode out of catchment as transferred
    # ???

    df_eof = df_eos.drop(columns=["site"])
    df_eof = df_eof.reset_index(drop=True)
    df = df.merge(
        df_eof[
            [
                "subject_identifier",
                "offstudy_datetime",
                "offstudy_reason",
                "other_offstudy_reason",
                "site_id",
            ]
        ],
        how="left",
        on=["subject_identifier", "site_id"],
    )

    df["country"] = df["site_id"].apply(lambda x: sites.get(x).country.lower())

    return df
