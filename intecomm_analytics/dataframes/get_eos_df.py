import pandas as pd
from django_pandas.io import read_frame
from edc_pdutils.dataframes import get_eos, get_subject_visit

from intecomm_prn.models import SubjectTransfer


def get_eos_df() -> pd.DataFrame:
    """
    df = get_eos_df()

    # look at transfers and last attended visit
    df[(df.transfer_reason.notna())]

    """
    df_eos = get_eos("intecomm_prn.endofstudy")
    df_visit = get_subject_visit("intecomm_subject.subjectvisit")
    df_last_visit = (
        df_visit.groupby("subject_identifier")
        .agg({"last_visit_code": "max", "last_visit_datetime": "max"})
        .reset_index()
    )

    df_eos = df_eos.merge(df_last_visit, on="subject_identifier", how="left")
    df_transfer = read_frame(
        SubjectTransfer.objects.values(
            "subject_identifier",
            "transfer_date",
            # "transfer_reason",
            "transfer_reason_other",
        ).all(),
        verbose=False,
    )
    df_transfer["transferred"] = 1
    df_reasons = read_frame(
        SubjectTransfer.objects.values("subject_identifier", "transfer_reason__name").all()
    )
    df_reasons["num"] = 1
    df_reasons = df_reasons.pivot_table(
        index="subject_identifier", columns="transfer_reason__name", values="num"
    ).reset_index()
    df_reasons = df_reasons.fillna(0)

    df_transfer = df_transfer.rename(columns={"transfer_reason": "transfer_reason_id"})
    df_transfer["transfer_date"] = df_transfer["transfer_date"].apply(pd.to_datetime)
    df_transfer["transfer_date"] = df_transfer["transfer_date"].dt.floor("d")
    df_transfer = df_transfer.merge(df_reasons, on="subject_identifier", how="left")
    df_transfer = df_transfer.reset_index(drop=True)

    df_eos = df_eos.merge(
        df_transfer,
        on="subject_identifier",
        how="left",
    )
    df_eos["transferred"] = df_eos["transferred"].fillna(0)

    return df_eos
