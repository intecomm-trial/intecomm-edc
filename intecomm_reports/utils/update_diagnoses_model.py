from datetime import date

from django.db.models import Count, Min
from edc_dx.diagnoses import (
    ClinicalReviewBaselineRequired,
    Diagnoses,
    InitialReviewRequired,
)
from edc_pdutils.model_to_dataframe import ModelToDataframe
from edc_utils import get_utcnow
from tqdm import tqdm

from intecomm_subject.models import SubjectVisit
from intecomm_subject.utils import recalculate_dx_calculated_date

from ..models import Diagnoses as DiagnosesModel


def export_diagnoses_model(path: str | None = None):
    m = ModelToDataframe(model="intecomm_reports.diagnoses")
    df = m.dataframe
    df["hiv_baseline"] = 0
    df["htn_baseline"] = 0
    df["dm_baseline"] = 0
    df.loc[(df["hiv_dx_date"] < df["baseline_date"]) & (df["hiv"] == 1), "hiv_baseline"] = 1
    df.loc[(df["htn_dx_date"] < df["baseline_date"]) & (df["htn"] == 1), "htn_baseline"] = 1
    df.loc[(df["dm_dx_date"] < df["baseline_date"]) & (df["dm"] == 1), "dm_baseline"] = 1
    df["condition_count"] = df[["hiv_baseline", "htn_baseline", "dm_baseline"]].sum(axis=1)
    if path:
        df.to_csv(
            path,
            columns=[
                "subject_identifier",
                "baseline_date",
                "hiv",
                "htn",
                "dm",
                "hiv_dx_date",
                "htn_dx_date",
                "dm_dx_date",
                "hiv_baseline",
                "htn_baseline",
                "dm_baseline",
                "condition_count",
            ],
            index=False,
        )
    return df


def update_diagnoses_model(delete_all: bool | None = None, path: str = None):
    """Calculate the diagnoses of each participant who has completed
    a baseline visit.

    To be considered having completed the baseline visit, the
    ClinicalReviewBaseline and the corresponding IntialReview forms
    must be complete.

    Protocol requires participants be diagnosed at least 6m ago and
    stable in care for at least 6 months. When querying the InitialReview
    forms, the diagnosis date must be at least 182 days prior to the
    baseline visit date.
    """
    errors = []
    if delete_all:
        DiagnosesModel.objects.all().delete()
    qs = (
        SubjectVisit.objects.values("subject_identifier", "site_id")
        .annotate(
            Count("subject_identifier", distinct=True),
            Count("site_id", distinct=True),
        )
        .order_by("subject_identifier")
        .annotate(Min("report_datetime"))
    )
    total = qs.count()
    for subject_visit in tqdm(qs, total=total):
        subject_identifier = subject_visit.get("subject_identifier")
        site_id = subject_visit.get("site_id")
        baseline_date = subject_visit.get("report_datetime__min").date()
        try:
            dx = Diagnoses(
                subject_identifier=subject_identifier,
                report_datetime=get_utcnow(),
                lte=True,
            )
        except ClinicalReviewBaselineRequired as e:
            errors.append(f"{subject_identifier}: {e}")
        else:
            errors.extend(
                update_diagnoses_instance(dx, subject_identifier, site_id, baseline_date)
            )
    for err in errors:
        print(err)


def update_diagnoses_instance(
    dx: Diagnoses,
    subject_identifier: str = None,
    site_id: str = None,
    baseline_date: date = None,
) -> list:
    """Updates for a single condition.

    Called by `update_diagnoses_model`.
    """
    errors = []
    obj, _ = DiagnosesModel.objects.get_or_create(
        subject_identifier=subject_identifier, site_id=site_id
    )
    obj.baseline_date = baseline_date
    try:
        initial_reviews = dx.initial_reviews
    except InitialReviewRequired:
        errors.append(f"{obj.subject_identifier}: initial_reviews not found!")
    else:
        for prefix in dx.diagnosis_labels:
            if initial_review := initial_reviews.get(prefix):
                recalculate_dx_calculated_date(
                    models={prefix: initial_review.__class__},
                    subject_identifier=obj.subject_identifier,
                )
                initial_review.refresh_from_db()
                if dx_date := (
                    getattr(initial_review, "dx_date")
                    or getattr(initial_review, "dx_calculated_date")
                ):
                    setattr(obj, prefix, True)
                    setattr(obj, f"{prefix}_dx_date", dx_date)
                    dx_days = (dx_date - obj.baseline_date).days
                    setattr(obj, f"{prefix}_dx_days", dx_days)
                else:
                    errors.append(
                        f"{obj.subject_identifier}: "
                        f"`dx_calculated_date` is None. Got {prefix}: "
                        f"{getattr(initial_review, 'dx_date')}"
                        f"{getattr(initial_review, 'dx_ago')}"
                    )
                    obj.comment = ",".join(errors)
                    setattr(obj, prefix, False)
                    setattr(obj, f"{prefix}_dx_date", None)
                    setattr(obj, f"{prefix}_dx_days", None)

    obj.save()
    return errors
