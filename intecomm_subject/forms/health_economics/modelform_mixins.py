from edc_constants.constants import YES
from edc_crf.utils import raise_if_crf_does_not_exist
from edc_dx_review.utils import raise_if_clinical_review_does_not_exist

from ...models import (
    HealthEconomicsAssets,
    HealthEconomicsHouseholdHead,
    HealthEconomicsIncome,
    HealthEconomicsProperty,
)


class HealthEconomicsModelFormMixin:
    def clean(self):
        raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        self.raise_if_he_household_head_required()
        self.raise_if_he_patient_required()
        self.raise_if_he_assets_required()
        self.raise_if_he_property_required()
        return super().clean()

    @property
    def household_head(self):
        return HealthEconomicsHouseholdHead.objects.get(
            subject_visit__subject_identifier=self.subject_identifier
        )

    def raise_if_he_household_head_required(self):
        if self._meta.model != HealthEconomicsHouseholdHead:
            raise_if_crf_does_not_exist(
                self.cleaned_data.get("subject_visit"),
                model="intecomm_subject.healtheconomicshouseholdhead",
            )

    def raise_if_he_patient_required(self):
        if self.household_head.hoh != YES and self._meta.model in [
            HealthEconomicsAssets,
            HealthEconomicsIncome,
            HealthEconomicsProperty,
        ]:
            raise_if_crf_does_not_exist(
                self.cleaned_data.get("subject_visit"),
                model="intecomm_subject.healtheconomicspatient",
            )

    def raise_if_he_assets_required(self):
        if self._meta.model in [
            HealthEconomicsIncome,
            HealthEconomicsProperty,
        ]:
            raise_if_crf_does_not_exist(
                self.cleaned_data.get("subject_visit"),
                model="intecomm_subject.healtheconomicsassets",
            )

    def raise_if_he_property_required(self):
        if self._meta.model in [
            HealthEconomicsIncome,
        ]:
            raise_if_crf_does_not_exist(
                self.cleaned_data.get("subject_visit"),
                model="intecomm_subject.healtheconomicsproperty",
            )
