from pathlib import Path

import pandas as pd

from .intecomm_gee_model import IDENTITY_BINOMIAL, IntecommGeeModel

__all__ = ["run_gee_identity_link_model"]


def run_gee_identity_link_model(
    df_main: pd.DataFrame,
    col: str,
    cohort: list[str],
    as_percentage: bool = False,
    path: Path | None = None,
):
    gee_model = IntecommGeeModel(
        df_main,
        col,
        cohort,
        family_label=IDENTITY_BINOMIAL,
        as_percentage=as_percentage,
    )
    unadjusted, adjusted = gee_model.run()
    if path:
        gee_model.save_to_pdf(path=path)
    else:
        gee_model.print()
    return unadjusted, adjusted
