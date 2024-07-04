import numpy as np
import pandas as pd
from django.apps import apps as django_apps
from django_pandas.io import read_frame
from edc_utils import get_utcnow
from edc_visit_schedule.models import SubjectScheduleHistory

from intecomm_subject.models import HivInitialReview, HivReview

from .models import Diagnoses as DiagnosesModel
from .utils import update_diagnoses_model


class VlSummary:

    def __init__(
        self,
        baseline_months: int | None = None,
        endline_months: int | None = None,
        skip_update_dx: bool | None = None,
    ):
        if not skip_update_dx:
            update_diagnoses_model(delete_all=True)
        self._dfdx: pd.DataFrame = pd.DataFrame()
        self._df_initial_review: pd.DataFrame = pd.DataFrame()
        self._df_review: pd.DataFrame = pd.DataFrame()
        self.baseline_months = baseline_months or 3
        self.endline_months = endline_months or 9

    def to_dataframe(self) -> pd.DataFrame:
        """Prepare and return final df"""
        # merge dxdf with df1 (from hiv initial review)
        df = pd.merge(self.dfdx, self.df_initial_review, on="subject_identifier", how="left")
        # consider as baseline vl if 0m or earlier
        df["baseline_vl"] = df[
            df["baseline_date"] + pd.DateOffset(months=self.baseline_months)
            >= df["drawn_date"]
        ]["vl"]
        df["baseline_vl_date"] = df[
            df["baseline_date"] + pd.DateOffset(months=self.baseline_months)
            >= df["drawn_date"]
        ]["drawn_date"]

        # consider as endline vl if 6m or later
        df["endline_vl"] = df[
            df["drawn_date"] > df["baseline_date"] + pd.DateOffset(months=self.endline_months)
        ]["vl"]
        df["endline_vl_date"] = df[
            df["drawn_date"] > df["baseline_date"] + pd.DateOffset(months=self.endline_months)
        ]["drawn_date"]

        # merge df with vls from hiv review
        # this adds cols vl1, vl1_date, vl2, vl2_date
        df = pd.merge(df, self.df_review, on="subject_identifier", how="left")

        # null out vl1 and vl2 if same date as baseline_vl date
        df.loc[df.baseline_vl_date == df.vl1_date, ["vl1", "vl1_date"]] = [np.nan, pd.NaT]
        df.loc[df.baseline_vl_date == df.vl2_date, ["vl2", "vl2_date"]] = [np.nan, pd.NaT]

        # fill any missing baseline
        df[["baseline_vl", "baseline_vl_date"]] = df.apply(
            lambda row: self.get_best_baseline_vl_and_date(row, months=self.baseline_months),
            axis=1,
        ).to_list()

        # fill missing endlines
        df[["endline_vl", "endline_vl_date"]] = df.apply(
            lambda row: self.get_best_endline_vl_and_date(row, months=self.endline_months),
            axis=1,
        ).to_list()

        df["next_vl_date"] = df.apply(
            lambda row: (
                row["last_vl_date"] + pd.DateOffset(months=12)
                if pd.notna(row["last_vl_date"])
                else row["baseline_vl_date"] + pd.DateOffset(months=12)
            ),
            axis=1,
        )
        df["expected"] = df.apply(
            lambda row: self.get_expected_endline_vl_and_date(row), axis=1
        )

        df["offset"] = df["next_vl_date"].dt.to_period("M") - df[
            "offschedule_date"
        ].dt.to_period("M")
        df["offset"] = df["offset"].apply(lambda x: x.n if pd.notna(x) else np.nan)
        return df

    def to_model(self, model: str | None = None):
        df = self.to_dataframe()
        model_cls = django_apps.get_model(model or "intecomm_reports.vlsummary")
        model_cls.objects.all().delete()
        model_cls.objects.bulk_create(
            [
                model_cls(
                    subject_identifier=row["subject_identifier"],
                    site_id=row["site_id"],
                    baseline_date=(
                        None if pd.isna(row["baseline_date"]) else row["baseline_date"]
                    ),
                    baseline_vl=None if pd.isna(row["baseline_vl"]) else row["baseline_vl"],
                    baseline_vl_date=(
                        None if pd.isna(row["baseline_vl_date"]) else row["baseline_vl_date"]
                    ),
                    endline_vl=None if pd.isna(row["endline_vl"]) else row["endline_vl"],
                    endline_vl_date=(
                        None if pd.isna(row["endline_vl_date"]) else row["endline_vl_date"]
                    ),
                    offschedule_date=(
                        None if pd.isna(row["offschedule_date"]) else row["offschedule_date"]
                    ),
                    last_vl_date=(
                        None if pd.isna(row["last_vl_date"]) else row["last_vl_date"]
                    ),
                    next_vl_date=(
                        None if pd.isna(row["next_vl_date"]) else row["next_vl_date"]
                    ),
                    expected=row["expected"],
                    offset=None if pd.isna(row["offset"]) else row["offset"],
                )
                for _, row in df.iterrows()
            ]
        )

    @property
    def dfdx(self) -> pd.DataFrame:
        """DiagnosesModel with offschedule as df.
        (update this model first!)
        """
        if self._dfdx.empty:
            qs = (
                DiagnosesModel.objects.values(
                    "subject_identifier",
                    "site__id",
                    "hiv",
                    "hiv_dx_date",
                    "hiv_dx_days",
                    "baseline_date",
                )
                .filter(hiv=1)
                .order_by("subject_identifier")
            )
            dfdx = read_frame(qs)
            dfdx.rename(columns={"site__id": "site_id"}, inplace=True)
            dfdx["baseline_date"] = dfdx["baseline_date"].astype("datetime64[ns]")
            dfdx["hiv_dx_date"] = dfdx["hiv_dx_date"].astype("datetime64[ns]")
            # merge in offschedule
            qs = SubjectScheduleHistory.objects.all()
            dfoff = read_frame(qs, fieldnames=["subject_identifier", "offschedule_datetime"])
            dfoff["offschedule_date"] = dfoff["offschedule_datetime"].dt.date
            dfoff["offschedule_date"] = dfoff["offschedule_date"].astype("datetime64[ns]")
            dfoff.drop(columns=["offschedule_datetime"], inplace=True)
            self._dfdx = pd.merge(dfdx, dfoff, on="subject_identifier")
        return self._dfdx

    @property
    def df_initial_review(self) -> pd.DataFrame:
        """HivInitialReview (df1).

        append empty cols to be populated
        """
        if self._df_initial_review.empty:
            df = self.get_review_model_as_df(HivInitialReview)
            df["baseline_vl"] = np.nan
            df["baseline_vl_date"] = pd.NaT
            df["endline_vl"] = np.nan
            df["endline_vl_date"] = pd.NaT
            self._df_initial_review = df
        return self._df_initial_review

    @property
    def df_review(self) -> pd.DataFrame:
        """HivReview (df1)"""
        if self._df_review.empty:
            df = self.get_review_model_as_df(HivReview)
            self._df_review = self.pivot_first_last_vl(df)
        return self._df_review

    @staticmethod
    def get_review_model_as_df(model_cls):
        qs = model_cls.objects.values(
            "subject_visit__subject_identifier",
            "has_vl",
            "vl",
            "drawn_date",
            "report_datetime",
        ).all()
        df = read_frame(
            qs,
            fieldnames=[
                "subject_visit__subject_identifier",
                "vl",
                "drawn_date",
                "report_datetime",
            ],
        )
        df.rename(
            columns={
                "subject_visit__subject_identifier": "subject_identifier",
                "site__id": "site_id",
            },
            inplace=True,
        )
        # vl column, replace nulls with NaN
        df.loc[df["vl"].isnull(), "vl"] = np.nan

        # report date
        df["report_date"] = pd.to_datetime(df["report_datetime"]).dt.date
        df["report_date"] = df["report_date"].astype("datetime64[ns]")
        df = df.drop("report_datetime", axis=1)

        # replace baseline drawn date with report date if drawn date is None
        df.loc[df["drawn_date"].isnull(), "drawn_date"] = df["report_date"]
        df["drawn_date"] = df["drawn_date"].astype("datetime64[ns]")
        return df

    @staticmethod
    def pivot_first_last_vl(df: pd.DataFrame) -> pd.DataFrame:
        # get rows with non-null VL, select first drawn vl and last drawn vl
        # ... get rows with non-null VL
        dftmp = df[df.vl.notna()].reset_index(drop=True)
        # ... select first drawn vl
        df_first = (
            dftmp.sort_values(by="vl").groupby("subject_identifier", as_index=False).first()
        )
        df_first.drop(columns="report_date", inplace=True)
        df_first.rename(columns={"vl": "vl1", "drawn_date": "vl1_date"}, inplace=True)
        # ... select last drawn vl
        df_last = (
            dftmp.sort_values(by="vl").groupby("subject_identifier", as_index=False).last()
        )
        df_last.drop(columns="report_date", inplace=True)
        df_last.rename(columns={"vl": "vl2", "drawn_date": "vl2_date"}, inplace=True)
        df_last["last_vl"] = df_last["vl2"]
        df_last["last_vl_date"] = df_last["vl2_date"]
        # null out vl2 if same date as vl1
        df = pd.merge(df_first, df_last, on="subject_identifier", how="left")
        df.loc[df.vl1_date == df.vl2_date, ["vl2", "vl2_date"]] = [np.nan, pd.NaT]
        return df

    @staticmethod
    def get_expected_endline_vl_and_date(row) -> bool:
        value = True
        if pd.notna(row["next_vl_date"]) & pd.notna(row["offschedule_date"]):
            value = pd.Timestamp(row["next_vl_date"]) <= pd.Timestamp(
                row["offschedule_date"] + pd.DateOffset(months=3)
            )
        elif pd.notna(row["next_vl_date"]) & pd.isna(row["offschedule_date"]):
            value = row["next_vl_date"].date() <= get_utcnow().date()
        return value

    @staticmethod
    def get_best_baseline_vl_and_date(row, months: int = None) -> tuple[pd.Series, pd.Series]:
        values = row["baseline_vl"], row["baseline_vl_date"]
        if pd.isna(row["baseline_vl"]):
            if pd.notna(row["vl1"]) & pd.notna(row["vl2"]):
                if (
                    row["vl2_date"] < row["vl1_date"]
                    and row["baseline_date"] + pd.DateOffset(months=months) >= row["vl2_date"]
                ):
                    values = row["vl2"], row["vl2_date"]
                elif row["baseline_date"] + pd.DateOffset(months=months) >= row["vl1_date"]:
                    values = row["vl1"], row["vl1_date"]
            elif (
                pd.notna(row["vl1"])
                and row["baseline_date"] + pd.DateOffset(months=months) >= row["vl1_date"]
            ):
                values = row["vl1"], row["vl1_date"]
        return values

    @staticmethod
    def get_best_endline_vl_and_date(row, months: int = None) -> tuple[pd.Series, pd.Series]:
        values = row["endline_vl"], row["endline_vl_date"]
        if pd.isna(row["endline_vl"]):
            if pd.notna(row["vl1"]) & pd.notna(row["vl2"]):
                if (
                    row["vl2_date"] > row["vl1_date"]
                    and row["baseline_date"] + pd.DateOffset(months=months) < row["vl2_date"]
                ):
                    values = row["vl2"], row["vl2_date"]
                elif row["baseline_date"] + pd.DateOffset(months=months) < row["vl1_date"]:
                    values = row["vl1"], row["vl1_date"]
            elif (
                pd.notna(row["vl1"])
                and row["baseline_date"] + pd.DateOffset(months=months) < row["vl1_date"]
            ):
                values = row["vl1"], row["vl1_date"]
        return values
