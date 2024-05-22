from django.core.management import BaseCommand
from django.db.models import Count
from edc_dx import Diagnoses
from edc_dx.diagnoses import ClinicalReviewBaselineRequired, InitialReviewRequired
from edc_utils import get_utcnow
from tqdm import tqdm

from intecomm_subject.models import SubjectVisit
from intecomm_subject.models.dm.dm_current_conditions import DmCurrentConditions


def update_conditions():
    errors = []
    qs = (
        SubjectVisit.objects.values("subject_identifier", "site_id")
        .annotate(Count("subject_identifier", distinct=True), Count("site_id", distinct=True))
        .order_by("subject_identifier")
    )
    total = qs.count()
    for obj in tqdm(qs, total=total):
        current_condition, _ = DmCurrentConditions.objects.get_or_create(
            subject_identifier=obj.get("subject_identifier"), site_id=obj.get("site_id")
        )
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
                pass
            else:
                for prefix in diagnoses.diagnosis_labels:
                    if initial_review := initial_reviews.get(prefix):
                        if dx_date := getattr(initial_review, "dx_calculated_date"):
                            setattr(current_condition, prefix, 1)
                            setattr(current_condition, f"{prefix}_dx_date", dx_date)
                        else:
                            errors.append(
                                f"{current_condition.subject_identifier}: "
                                "`dx_calculated_date` is None"
                            )
                            setattr(current_condition, prefix, 0)
                            setattr(current_condition, f"{prefix}_dx_date", None)
            current_condition.save()
    for err in errors:
        print(err)


class Command(BaseCommand):
    def __init__(self, **kwargs):
        self.site_ids: list[int] = []
        super().__init__(**kwargs)

    def handle(self, *args, **options):
        update_conditions()
