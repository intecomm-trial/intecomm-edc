from edc_dx_review.utils import raise_if_clinical_review_does_not_exist
from edc_he.forms import HealthEconomicsModelFormMixin as Base


class HealthEconomicsModelFormMixin(Base):
    def clean(self):
        raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        return super().clean()
