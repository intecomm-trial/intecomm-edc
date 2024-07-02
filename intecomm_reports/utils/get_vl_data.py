from dataclasses import dataclass, field
from datetime import date

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django_pandas.io import read_frame
from edc_constants.constants import YES
from tqdm import tqdm

from intecomm_prn.models import OffScheduleComm, OffScheduleInte
from intecomm_subject.models import HivInitialReview, HivReview

from ..models import Diagnoses as DiagnosesModel
from ..models import VlSummary


@dataclass
class Vl:
    baseline_vl: int
    baseline_vl_date: date
    endline_vl: int
    endline_vl_date: date


@dataclass
class Data:
    subject_identifier: str
    baseline_date: date
    dx_date: date
    baseline_vl: int | None = field(default=None)
    baseline_vl_date: date | None = field(default=None)
    endline_vl: int | None = field(default=None)
    endline_vl_date: date | None = field(default=None)

    @property
    def offschedule_date(self) -> date:
        offschedule_date = None
        try:
            obj = OffScheduleComm.objects.get(subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            try:
                obj = OffScheduleInte.objects.get(subject_identifier=self.subject_identifier)
            except ObjectDoesNotExist:
                pass
            else:
                offschedule_date = obj.offschedule_datetime.date()
        else:
            offschedule_date = obj.offschedule_datetime.date()
        return offschedule_date

    def as_tuple(self):
        return (
            self.subject_identifier,
            self.baseline_date,
            self.dx_date,
            self.baseline_vl,
            self.baseline_vl_date,
            self.endline_vl,
            self.endline_vl_date,
            self.offschedule_date,
        )


def get_vl_columns(review_obj: HivInitialReview | HivReview, baseline_date: date) -> Vl:
    drawn_date = review_obj.drawn_date or review_obj.report_datetime.date()
    baseline_vl = (
        review_obj.vl if drawn_date <= baseline_date + relativedelta(months=3) else np.nan
    )
    baseline_vl_date = drawn_date if drawn_date <= baseline_date else pd.NaT
    endline_vl = (
        review_obj.vl if drawn_date >= baseline_date + relativedelta(months=6) else np.nan
    )
    endline_vl_date = (
        drawn_date if drawn_date >= baseline_date + relativedelta(months=6) else pd.NaT
    )
    return Vl(baseline_vl, baseline_vl_date, endline_vl, endline_vl_date)


def vl_summary_to_dataframe(
    baseline_months: int | None = None,
    endline_months: int | None = None,
    path: str | None = None,
) -> tuple[pd.DataFrame, ...]:
    baseline_months = baseline_months or 3
    endline_months = endline_months or 9

    # DiagnosesModel (update this model first!)
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

    # HivInitialReview (df1)
    df1 = get_review_model_as_df(HivInitialReview)

    # append empty cols to be populated
    df1["baseline_vl"] = np.nan
    df1["baseline_vl_date"] = pd.NaT
    df1["endline_vl"] = np.nan
    df1["endline_vl_date"] = pd.NaT

    # merge dxdf with df1 (from hiv initial review)
    df = pd.merge(dfdx, df1, on="subject_identifier", how="left")

    # consider as baseline vl if 0m or earlier
    df["baseline_vl"] = df[
        df["baseline_date"] + pd.DateOffset(months=baseline_months) >= df["drawn_date"]
    ]["vl"]
    df["baseline_vl_date"] = df[
        df["baseline_date"] + pd.DateOffset(months=baseline_months) >= df["drawn_date"]
    ]["drawn_date"]

    # consider as endline vl if 6m or later
    df["endline_vl"] = df[
        df["baseline_date"] + pd.DateOffset(months=endline_months) < df["drawn_date"]
    ]["vl"]
    df["endline_vl_date"] = df[
        df["baseline_date"] + pd.DateOffset(months=endline_months) < df["drawn_date"]
    ]["drawn_date"]

    # HivReview (df2)
    df2 = get_review_model_as_df(HivReview)
    df2 = pivot_first_last_vl(df2)

    # merge df with vls from hiv review
    # this adds cols vl1, vl1_date, vl2, vl2_date
    df = pd.merge(df, df2, on="subject_identifier", how="left")

    # null out vl1 and vl2 if same date as baseline_vl date
    df.loc[df.baseline_vl_date == df.vl1_date, ["vl1", "vl1_date"]] = [np.nan, pd.NaT]
    df.loc[df.baseline_vl_date == df.vl2_date, ["vl2", "vl2_date"]] = [np.nan, pd.NaT]

    # fill any missing baseline
    df[["baseline_vl", "baseline_vl_date"]] = df.apply(
        lambda row: get_best_baseline_vl_and_date(row, months=baseline_months), axis=1
    ).to_list()

    # fill missing endlines
    df[["endline_vl", "endline_vl_date"]] = df.apply(
        lambda row: get_best_endline_vl_and_date(row, months=endline_months), axis=1
    ).to_list()

    return df, dfdx, df1, df2


def get_best_baseline_vl_and_date(row, months: int = None):
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


def get_best_endline_vl_and_date(row, months: int = None):
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


def get_review_model_as_df(model_cls):
    qs = model_cls.objects.values(
        "subject_visit__subject_identifier", "has_vl", "vl", "drawn_date", "report_datetime"
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


def vl_summary_to_table(request=None, **kwargs):
    df, _, _, _ = vl_summary_to_dataframe(**kwargs)
    # try:
    #     site_id = request.site.id
    # except AttributeError:
    #     VlSummary.objects.all().delete()
    # else:
    #     VlSummary.objects.filter(site_id=site_id).delete()
    #     df = df[df["site_id"]==site_id]
    VlSummary.objects.all().delete()
    VlSummary.objects.bulk_create(
        [
            VlSummary(
                subject_identifier=row["subject_identifier"],
                site_id=row["site_id"],
                baseline_date=None if pd.isna(row["baseline_date"]) else row["baseline_date"],
                baseline_vl=None if pd.isna(row["baseline_vl"]) else row["baseline_vl"],
                baseline_vl_date=(
                    None if pd.isna(row["baseline_vl_date"]) else row["baseline_vl_date"]
                ),
                endline_vl=None if pd.isna(row["endline_vl"]) else row["endline_vl"],
                endline_vl_date=(
                    None if pd.isna(row["endline_vl_date"]) else row["endline_vl_date"]
                ),
            )
            for _, row in df.iterrows()
        ]
    )


def pivot_first_last_vl(df: pd.DataFrame) -> pd.DataFrame:
    # get rows with non-null VL, select first drawn vl and last drawn vl
    # ... get rows with non-null VL
    dftmp = df[df.vl.notna()].reset_index(drop=True)
    # ... select first drawn vl
    df_first = dftmp.sort_values(by="vl").groupby("subject_identifier", as_index=False).first()
    df_first.drop(columns="report_date", inplace=True)
    df_first.rename(columns={"vl": "vl1", "drawn_date": "vl1_date"}, inplace=True)
    # ... select last drawn vl
    df_last = dftmp.sort_values(by="vl").groupby("subject_identifier", as_index=False).last()
    df_last.drop(columns="report_date", inplace=True)
    df_last.rename(columns={"vl": "vl2", "drawn_date": "vl2_date"}, inplace=True)
    # null out vl2 if same date as vl1
    df = pd.merge(df_first, df_last, on="subject_identifier", how="left")
    df.loc[df.vl1_date == df.vl2_date, ["vl2", "vl2_date"]] = [np.nan, pd.NaT]
    return df


def get_vl_data(path=None) -> pd.DataFrame:
    qs = DiagnosesModel.objects.filter(hiv=1).order_by("subject_identifier")
    total = qs.count()
    all_data = []
    for diagnoses in tqdm(qs, total=total):
        data = Data(
            diagnoses.subject_identifier,
            diagnoses.baseline_date,
            diagnoses.hiv_dx_date,
        )
        try:
            hiv_initial_review = HivInitialReview.objects.get(
                subject_visit__subject_identifier=diagnoses.subject_identifier
            )
        except ObjectDoesNotExist:
            pass
        else:
            if hiv_initial_review.has_vl == YES:
                vl = get_vl_columns(hiv_initial_review, diagnoses.baseline_date)
                data.dx_date = diagnoses.hiv_dx_date
                data.baseline_vl = vl.baseline_vl
                data.baseline_vl_date = vl.baseline_vl_date
        for hiv_review in HivReview.objects.filter(
            subject_visit__subject_identifier=diagnoses.subject_identifier
        ):
            if hiv_review.has_vl == YES:
                vl = get_vl_columns(hiv_review, diagnoses.baseline_date)
                if not data.baseline_vl:
                    data.baseline_vl = vl.baseline_vl
                    data.baseline_vl_date = vl.baseline_vl_date
                if not data.endline_vl:
                    data.endline_vl = vl.endline_vl
                    data.endline_vl_date = vl.endline_vl_date
        all_data.append(data.as_tuple())
    np_data = np.array(
        all_data,
        # dtype=[
        #     ("subject_identifier", "object"),
        #     ("baseline_date", "datetime64[ns]"),
        #     ("dx_date", "datetime64[ns]"),
        #     ("baseline_vl_value", "float64"),
        #     ("baseline_vl_date", "datetime64[ns]"),
        #     ("endline_vl_value", "float64"),
        #     ("endline_vl_date", "datetime64[ns]"),
        # ],
    )
    df = pd.DataFrame(
        np_data,
        columns=[
            "subject_identifier",
            "baseline_date",
            "dx_date",
            "baseline_vl_value",
            "baseline_vl_date",
            "endline_vl_value",
            "endline_vl_date",
            "offschedule_date",
        ],
    )

    # df["baseline"] = 0
    # df.loc[df["vl_date"] <= df["baseline_date"], "baseline"] = 1
    # df["endline"] = 0
    # df.loc[df["vl_date"] >= df["baseline_date"] + pd.DateOffset(months=6), "endline"] = 1

    if path:
        df.to_csv(path_or_buf=path, index=False)
    return df
