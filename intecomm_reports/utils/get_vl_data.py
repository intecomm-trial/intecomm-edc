from dataclasses import dataclass, field
from datetime import date

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES
from tqdm import tqdm

from intecomm_prn.models import OffScheduleComm, OffScheduleInte
from intecomm_subject.models import HivInitialReview, HivReview

from ..models import Diagnoses as DiagnosesModel


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
    np_data = np.array(all_data)
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
    if path:
        df.to_csv(path_or_buf=path, index=False)
    return df
