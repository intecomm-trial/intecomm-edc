import io
import sys
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
from intecomm_rando.constants import COMMUNITY_ARM, FACILITY_ARM
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Preformatted, SimpleDocTemplate

IDENTITY_BINOMIAL = "identity-binomial"
GAUSSIAN = "gaussian"

__all__ = ["IntecommGeeModel"]


class IntecommGeeModel:
    def __init__(
        self,
        df_raw: pd.DataFrame,
        col: str,
        cohort: list[str],
        family_label: str | None = None,
        as_percentage: bool | None = None,
    ):
        self.warn_msg = ""
        self.gee_results_unadjusted = None
        self.gee_results_adjusted = None
        self.col = col
        self.cohort = cohort
        self.perc_factor = 100 if as_percentage else 1

        self.family_label = family_label or IDENTITY_BINOMIAL
        if self.family_label == IDENTITY_BINOMIAL:
            self.family = sm.families.Binomial(link=sm.families.links.Identity())
            self.cov_struct = sm.cov_struct.Independence()
        elif self.family_label == GAUSSIAN:
            self.family = sm.families.Gaussian()
            self.cov_struct = sm.cov_struct.Independence()
        else:
            raise ValueError("Invalid family label")

        self.df_raw = df_raw.query("primary_cohort_str.isin(@self.cohort)").copy()
        self.df_model = self.prepare_df_model()

    def run(self) -> tuple:
        self.gee_results_unadjusted = self.fit_model(
            formula=f"{self.col} ~ arm",
        )
        self.gee_results_adjusted = self.fit_model(
            formula=f"{self.col} ~ arm+age_in_years+gender",
        )
        return self.gee_results_unadjusted, self.gee_results_adjusted

    def print(self):
        self._print("unadjusted", self.gee_results_unadjusted)
        self._print("adjusted", self.gee_results_adjusted)

    def save_to_pdf(self, path: Path):
        story = []
        filename = path / f"{self.col}.pdf"
        doc = SimpleDocTemplate(str(filename), pagesize=letter)
        for label, results in {
            "unadjusted": self.gee_results_unadjusted,
            "adjusted": self.gee_results_adjusted,
        }.items():
            buffer = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buffer
            self._print(label, results)
            sys.stdout = old_stdout
            content = buffer.getvalue()  # .encode("utf-8")
            styles = getSampleStyleSheet()
            preformatted_style = styles["Code"]
            story.append(Preformatted(content, preformatted_style))
            story.append(PageBreak())
        doc.build(story)
        print(f"\nModel results saved to {filename}")

    def prepare_df_model(self) -> pd.DataFrame:
        """Prepare the dataframe for use in the model.

        * filter for the cohort
        * relabel assignment into new col `arm`.
          GEE model assumes arms are alphabetical A:B where
          A is CONTROL and B is INTERVENTION
        * remove any null data and generate a message of what
          dropped
        * fix column types
        """
        # make a fresh copy
        df_model = self.df_raw.query("primary_cohort_str.isin(@self.cohort)").copy()

        # relabel assignment labels in new column
        df_model["arm"] = df_model["assignment"].apply(
            lambda x: "A-FACILITY" if x == FACILITY_ARM else "B-COMMUNITY"
        )

        # sort by group identifier
        df_model = df_model.sort_values(["group_identifier"]).reset_index(drop=True)

        # look for null data, remove and warn
        initial_rows = len(df_model)
        df_model = df_model.dropna(
            subset=[
                "group_identifier",
                "arm",
                "assignment",
                self.col,
                "gender",
                "age_in_years",
                "subject_identifier",
            ]
        )
        final_rows = len(df_model)
        if initial_rows > final_rows:
            self.warn_msg = (
                f"Dropped {initial_rows - final_rows} rows with missing data."
            )
        df_model = (
            df_model[
                [
                    "group_identifier",
                    "arm",
                    "assignment",
                    self.col,
                    "gender",
                    "age_in_years",
                    "subject_identifier",
                ]
            ]
            .copy()
            .reset_index(drop=True)
        )
        # fix_column_types
        if self.family_label == IDENTITY_BINOMIAL:
            df_model[self.col] = df_model[self.col].astype(int)
        elif self.family_label == GAUSSIAN:
            df_model[self.col] = df_model[self.col].astype(float)
        df_model["assignment"] = df_model["assignment"].astype("category")
        df_model["arm"] = df_model["arm"].astype("category")
        df_model["gender"] = df_model["gender"].astype("category")
        df_model["age_in_years"] = df_model["age_in_years"].astype(int)
        return df_model

    def fit_model(self, formula: str):
        model = sm.GEE.from_formula(
            formula,
            groups="group_identifier",
            data=self.df_model,
            family=self.family,
            cov_struct=self.cov_struct,
        )
        return model.fit()

    def _print(self, label: str, gee_results, buffer=None):
        if buffer:
            old_stdout = sys.stdout
            sys.stdout = buffer

        print("")
        print(f"GEE Model Results: {label.title()} for `{self.col}`")
        print("~" * len(f"GEE Model Results: {label.title()} for `{self.col}`"))
        print(f"\ncohort={self.cohort}\n")
        print(gee_results.summary())
        print("\n")

        risk_difference = gee_results.params["arm[T.B-COMMUNITY]"]
        conf_interval = gee_results.conf_int().loc["arm[T.B-COMMUNITY]"]
        p_value = gee_results.pvalues["arm[T.B-COMMUNITY]"]

        line_length = len(
            f"Crude Risk Diff (COMMUNITY vs. FACILITY): " f"{risk_difference:.4f}"
        )
        print(f"Simple summary: {label.title()}")
        print("+------------------------------------------------+")
        print(f"Crude Risk Diff (COMMUNITY vs. FACILITY): " f"{risk_difference:.4f}")
        print(f"95% CI: ({conf_interval[0]:.4f}, " f"{conf_interval[1]:.4f})")

        print(f"P-value: {p_value:.4f}")
        print("")

        print(f"Table cell contents: {label.title()}")
        print("+------------------------------------------------+")
        print(
            f"{risk_difference*self.perc_factor:.2f} "
            f"({conf_interval[0]*self.perc_factor:.2f}, "
            f"{conf_interval[1]*self.perc_factor:.2f})"
        )
        print(f"P={p_value:.4f}")
        if self.perc_factor == 100:
            print("Note: expressed as %")

        print("")
        if self.family_label == IDENTITY_BINOMIAL:
            for assignment in [COMMUNITY_ARM, FACILITY_ARM]:
                label = (
                    "COMMUNITY_ARM" if assignment == COMMUNITY_ARM else "FACILITY_ARM"
                )
                num = len(
                    self.df_model.query(f"{self.col}==1 and assignment==@assignment")
                )
                total = len(self.df_model.query("assignment==@assignment"))
                perc = (num / total) * 100
                print(f"{label}: {num}/{total} ({perc:.2f})")
                print("")
        elif self.family_label == GAUSSIAN:
            for assignment in [COMMUNITY_ARM, FACILITY_ARM]:
                label = (
                    "COMMUNITY_ARM" if assignment == COMMUNITY_ARM else "FACILITY_ARM"
                )
                describe = self.df_model.query("assignment==@assignment")[
                    self.col
                ].describe()
                print(
                    f"{label}: mean (std) {describe['mean']:.2f} "
                    f"({describe['std']:.2f}) n={describe['count']}"
                )
                print(
                    f"{label}: mean (min,max) {describe['mean']:.2f} "
                    f"n={describe['count']}"
                    f"({describe['min']:.2f},{describe['max']:.2f}) "
                    f"n={describe['count']}"
                )
                print(
                    f"{label}: mean (iqr) {describe['mean']:.2f} n={describe['count']}"
                    f"({describe['25%']:.2f},{describe['75%']:.2f}) "
                    f"n={describe['count']}"
                )
                print("")
        else:
            raise ValueError("Unhandled family label for extra stats ")

        # warnings for missing / excluded rows
        print(" ")
        print("Warnings")
        print("+------------------------------------------------+")
        print(self.warn_msg)
        for assignment in [COMMUNITY_ARM, FACILITY_ARM]:
            label = "COMMUNITY_ARM" if assignment == COMMUNITY_ARM else "FACILITY_ARM"
            dftmp = self.df_raw[
                (~self.df_raw.subject_identifier.isin(self.df_model.subject_identifier))
                & (self.df_raw.assignment == assignment)
            ][
                [
                    "subject_identifier",
                    "group_identifier",
                    self.col,
                    "gender",
                    "age_in_years",
                ]
            ]
            print(f"{len(dftmp)} {label}")
        print("")
        for assignment in [COMMUNITY_ARM, FACILITY_ARM]:
            label = "COMMUNITY_ARM" if assignment == COMMUNITY_ARM else "FACILITY_ARM"
            dftmp = self.df_raw[
                (~self.df_raw.subject_identifier.isin(self.df_model.subject_identifier))
                & (self.df_raw.assignment == assignment)
            ][
                [
                    "subject_identifier",
                    "group_identifier",
                    self.col,
                    "gender",
                    "age_in_years",
                ]
            ]
            print(f"{len(dftmp)} {label}")
            print(dftmp)
            print("")
        print("")
        print("=" * line_length)
        print("")
        if buffer:
            sys.stdout = old_stdout
