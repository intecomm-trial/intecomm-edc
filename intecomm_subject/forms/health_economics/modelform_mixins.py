from edc_dx_review.utils import raise_if_clinical_review_does_not_exist
from edc_he.forms import (
    HealthEconomicsModelFormMixin as BaseHealthEconomicsModelFormMixin,
)


class HealthEconomicsModelFormMixin(BaseHealthEconomicsModelFormMixin):
    def clean(self) -> dict:
        cleaned_data = super().clean()
        raise_if_clinical_review_does_not_exist(cleaned_data.get("subject_visit"))
        return cleaned_data
