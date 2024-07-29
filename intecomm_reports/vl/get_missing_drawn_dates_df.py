import pandas as pd
from django.apps import apps as django_apps
from edc_constants.constants import YES
from edc_pdutils.dataframes import get_crf


def get_missing_drawn_dates_df(model: str | None = None):
    # "intecomm_reports.missingvldrawdates"
    df_review = get_crf(
        "intecomm_subject.hivreview", subject_visit_model="intecomm_subject.subjectvisit"
    )
    df_review["baseline_date"] = pd.to_datetime(df_review["baseline_datetime"]).dt.date
    df_review["baseline_date"] = pd.to_datetime(df_review["baseline_date"])
    df_review["visit_date"] = pd.to_datetime(df_review["visit_datetime"]).dt.date
    df_review["visit_date"] = pd.to_datetime(df_review["visit_date"])

    df_missing_drawn_date2 = df_review[
        (df_review["has_vl"] == YES) & (df_review["drawn_date"].isna())
    ][
        [
            "subject_identifier",
            "site",
            "baseline_date",
            "visit_date",
            "visit_code",
            "vl",
            "drawn_date",
        ]
    ]
    df_missing_drawn_date2.reset_index()

    df_initial = get_crf(
        "intecomm_subject.hivinitialreview",
        subject_visit_model="intecomm_subject.subjectvisit",
    )
    df_initial["baseline_date"] = pd.to_datetime(df_initial["baseline_datetime"]).dt.date
    df_initial["baseline_date"] = pd.to_datetime(df_initial["baseline_date"])
    df_initial["visit_date"] = pd.to_datetime(df_initial["visit_datetime"]).dt.date
    df_initial["visit_date"] = pd.to_datetime(df_initial["visit_date"])

    df_missing_drawn_date1 = df_initial[
        (df_initial["has_vl"] == YES) & (df_initial["drawn_date"].isna())
    ][
        [
            "subject_identifier",
            "site",
            "baseline_date",
            "visit_date",
            "visit_code",
            "vl",
            "drawn_date",
        ]
    ]
    df_missing_drawn_date1.reset_index()

    df_missing_drawn_date = pd.concat([df_missing_drawn_date1, df_missing_drawn_date2])
    df_missing_drawn_date = df_missing_drawn_date.rename(columns={"site": "site_id"})
    df = df_missing_drawn_date.sort_values(["subject_identifier", "visit_code"])
    df.reset_index(drop=True)

    # refresh model class
    model_cls = django_apps.get_model(model)
    model_cls.objects.all().delete()
    model_cls.objects.bulk_create(
        model_cls(
            subject_identifier=row["subject_identifier"],
            site_id=row["site_id"],
            baseline_date=(None if pd.isna(row["baseline_date"]) else row["baseline_date"]),
            visit_date=(None if pd.isna(row["visit_date"]) else row["visit_date"]),
            visit_code=(None if pd.isna(row["visit_code"]) else row["visit_code"]),
            vl=(None if pd.isna(row["vl"]) else row["vl"]),
        )
        for _, row in df.iterrows()
    )
