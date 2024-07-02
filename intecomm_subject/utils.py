from edc_dx.diagnoses import DiagnosesError
from edc_dx_review.model_mixins.factory.calculate_date import update_calculated_date
from edc_model.utils import get_report_datetime_field_name
from edc_utils import get_utcnow
from tqdm import tqdm

from .models import DmInitialReview, HivInitialReview, HtnInitialReview


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
