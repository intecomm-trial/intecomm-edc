from pathlib import Path

import pandas as pd

from .intecomm_gee_model import GAUSSIAN, IntecommGeeModel

__all__ = ["run_gee_guassian_model"]


def run_gee_guassian_model(
    df_main: pd.DataFrame,
    col: str,
    cohort: list[str],
    path: Path | None = None,
):
    gee_model = IntecommGeeModel(df_main, col, cohort, family_label=GAUSSIAN)
    gee_model.run()
    gee_model.run()
    if path:
        gee_model.save_to_pdf(path=path)
    else:
        gee_model.print()
