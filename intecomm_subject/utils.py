from datetime import date

from django.db.models import Count, Min
from edc_dx.diagnoses import (
    ClinicalReviewBaselineRequired,
    Diagnoses,
    DiagnosesError,
    InitialReviewRequired,
)
from edc_dx_review.model_mixins.factory.calculate_date import update_calculated_date
from edc_model.utils import get_report_datetime_field_name
from edc_utils import get_utcnow
from tqdm import tqdm

from .models import (
    CurrentConditions,
    DmInitialReview,
    HivInitialReview,
    HtnInitialReview,
    SubjectVisit,
)


def recalculate_dx_calculated_date(
    models: dict | None = None, subject_identifier: str | None = None
):
    errors = []
    models = models or {
        "hiv": HivInitialReview,
        "htn": HtnInitialReview,
        "dm": DmInitialReview,
    }
    for fld_prefix, model_cls in models.items():
        opts = {}
        disable_tqdm = False
        if subject_identifier:
            opts = dict(subject_visit__subject_identifier=subject_identifier)
            disable_tqdm = True
        qs = model_cls.objects.filter(**opts)
        total = qs.count()
        for obj in tqdm(qs, total=total, disable=disable_tqdm):
            subject_identifier = obj.subject_visit.subject_identifier
            update_calculated_date(
                obj,
                fld_prefix="dx",
                reference_field=get_report_datetime_field_name(),
            )
            obj.modified = get_utcnow()
            obj.user_modified = "erikvw"
            try:
                obj.save_base(
                    update_fields=[
                        "dx_calculated_date",
                        "dx_date_is_estimated",
                        "modified",
                        "user_modified",
                    ]
                )
            except DiagnosesError as e:
                errors.append(f"{subject_identifier}. {e}")
    for err in errors:
        print(err)


def update_current_conditions(delete_all: bool | None = None):
    """Calculate the diagnoses of each participant who has completed
    a baseline visit.

    To be considered having completed the baseline visit, the
    ClinicalReviewBaseline and the corresponding IntialReview forms
    must be complete.

    Protocol requires participants be diagnosed at least 6m ago and
    stable in care for at least 6 months. When querying the InitialReview
    forms, the diagnosis date must be at least 180 days prior to the
    baseline visit date.
    """
    errors = []
    if delete_all:
        CurrentConditions.objects.all().delete()
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
    for obj in tqdm(qs, total=total):
        current_condition, _ = CurrentConditions.objects.get_or_create(
            subject_identifier=obj.get("subject_identifier"), site_id=obj.get("site_id")
        )
        baseline_date = obj.get("report_datetime__min").date()
        errors.extend(update_current_condition(current_condition, baseline_date))
    for err in errors:
        print(err)


def update_current_condition(current_condition, baseline_date: date) -> list:
    """Updates for a single condition.

    Called by `update_current_conditions`.
    """
    errors = []
    current_condition.baseline_date = baseline_date
    try:
        diagnoses = Diagnoses(
            subject_identifier=current_condition.subject_identifier,
            report_datetime=get_utcnow(),
            lte=True,
        )
    except ClinicalReviewBaselineRequired as e:
        errors.append(f"{current_condition.subject_identifier}: {e}")
    else:
        try:
            initial_reviews = diagnoses.initial_reviews
        except InitialReviewRequired:
            errors.append(
                f"{current_condition.subject_identifier}: initial_reviews not found!"
            )
        else:
            for prefix in diagnoses.diagnosis_labels:
                if initial_review := initial_reviews.get(prefix):
                    recalculate_dx_calculated_date(
                        models={prefix: initial_review.__class__},
                        subject_identifier=current_condition.subject_identifier,
                    )
                    initial_review.refresh_from_db()
                    if dx_date := (
                        getattr(initial_review, "dx_date")
                        or getattr(initial_review, "dx_calculated_date")
                    ):
                        setattr(current_condition, prefix, True)
                        setattr(current_condition, f"{prefix}_dx_date", dx_date)
                        dx_days = (dx_date - current_condition.baseline_date).days
                        setattr(current_condition, f"{prefix}_dx_days", dx_days)
                    else:
                        errors.append(
                            f"{current_condition.subject_identifier}: "
                            f"`dx_calculated_date` is None. Got {prefix}: "
                            f"{getattr(initial_review, 'dx_date')}"
                            f"{getattr(initial_review, 'dx_ago')}"
                        )
                        current_condition.comment = ",".join(errors)
                        setattr(current_condition, prefix, False)
                        setattr(current_condition, f"{prefix}_dx_date", None)
                        setattr(current_condition, f"{prefix}_dx_days", None)

    current_condition.save()
    return errors
