import pandas as pd
from edc_model import duration_to_date
from edc_pdutils.dataframes import get_subject_consent

from intecomm_consent.models import SubjectConsent


def duration_to_date_by_row(row: pd.Series, col: str = None):
    return duration_to_date(duration_text=row[col], reference_date=row["report_datetime"])


def get_consent_df(df: pd.DataFrame | None = None) -> pd.DataFrame:
    df = get_subject_consent(model_cls=SubjectConsent, extra_columns=["group_identifier"])
    return df
