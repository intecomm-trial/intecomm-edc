import pandas as pd
from django_pandas.io import read_frame
from edc_constants.constants import OTHER
from edc_pdutils.dataframes import get_eos, get_subject_visit

from intecomm_lists.models import TransferReasons
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
            "transfer_reason",
            "transfer_reason_other",
        ).all(),
        verbose=False,
    )
    df_transfer = df_transfer.rename(columns={"transfer_reason": "transfer_reason_id"})
    df_transfer["transfer_date"] = df_transfer["transfer_date"].apply(pd.to_datetime)
    df_transfer["transfer_date"] = df_transfer["transfer_date"].dt.floor("d")

    df_reasons = read_frame(TransferReasons.objects.values("id", "name", "display_name").all())
    df_reasons = df_reasons.rename(columns={"id": "transfer_reason_id"})
    df_reasons = df_reasons.reset_index(drop=True)

    df_transfer = df_transfer.merge(df_reasons, on="transfer_reason_id", how="left")
    df_transfer["transfer_reason"] = df_transfer.apply(
        lambda r: r["transfer_reason_other"] if r["name"] == OTHER else r["name"], axis=1
    )

    df_transfer = df_transfer.reset_index(drop=True)

    df_eos = df_eos.merge(
        df_transfer[["subject_identifier", "transfer_date", "transfer_reason"]],
        on="subject_identifier",
        how="left",
    )
    return df_eos
