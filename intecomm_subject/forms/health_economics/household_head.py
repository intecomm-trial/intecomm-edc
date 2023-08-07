from django import forms
from django.utils.html import format_html
from edc_consent.utils import get_consent_model_cls
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_dx_review.utils import raise_if_clinical_review_does_not_exist
from edc_he.constants import CHF, NHIF
from edc_he.form_validators import HealthEconomicsHouseholdHeadFormValidator
from edc_sites import get_sites_by_country
from edc_utils import age

from intecomm_sites import all_sites

from ...models import HealthEconomicsHouseholdHead
from ..mixins import CrfModelFormMixin


class HealthEconomicsHouseholdHeadForm(
    CrfSingletonModelFormMixin, CrfModelFormMixin, forms.ModelForm
):
    form_validator_cls = HealthEconomicsHouseholdHeadFormValidator

    def clean(self):
        self.raise_if_singleton_exists()
        raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        return super().clean()

    def clean_hoh_gender(self):
        hoh = self.cleaned_data.get("hoh")
        hoh_gender = self.cleaned_data.get("hoh_gender")
        if hoh and hoh == YES and hoh_gender and hoh_gender != self.subject_consent.gender:
            raise forms.ValidationError(
                "Mismatch. Subject is the head of household and "
                f"is {self.subject_consent.get_gender_display().lower()}."
            )
        return hoh_gender

    def clean_hoh_age(self):
        hoh = self.cleaned_data.get("hoh")
        hoh_age = self.cleaned_data.get("hoh_age")
        if hoh and hoh == YES and hoh_age:
            if (
                hoh_age
                != age(
                    self.subject_consent.dob, self.cleaned_data.get("report_datetime")
                ).years
            ):
                age_in_years = age(
                    self.subject_consent.dob, self.cleaned_data.get("report_datetime")
                ).years
                raise forms.ValidationError(
                    "Mismatch. Subject is the head of household and "
                    f"is {age_in_years} as of this report date."
                )
        return hoh_age

    def clean_hoh_insurance(self):
        hoh_insurance = self.cleaned_data.get("hoh_insurance")
        for obj in hoh_insurance.all():
            uganda_sites = get_sites_by_country(country="uganda", all_sites=all_sites)
            if obj.name in [NHIF, CHF] and self.related_visit.site_id in [
                s.site_id for s in uganda_sites
            ]:
                raise forms.ValidationError(
                    f"Invalid select for your country (Uganda). Got `{obj.display_name}`."
                )

        return hoh_insurance

    @property
    def subject_consent(self):
        return get_consent_model_cls().objects.get(subject_identifier=self.subject_identifier)

    class Meta:
        model = HealthEconomicsHouseholdHead
        fields = "__all__"
        help_texts = {
            "hoh_employment_type": format_html(
                '<div class="form-row"><OL><LI><b>Chief executives, managers, senior '
                "officials and legislators</b> </li>"
                "<LI><b>Professionals, technicians and associate professionals</b>  (e.g. "
                "science/engineering professionals, architects, nurses, doctors, teachers, "
                "technicians, construction/mining supervisors, etc.)</li>"
                "<LI><b>Clerks</b> (e.g. clerical support workers, receptionist, secretary, "
                "postman/woman etc.) </li>"
                "<LI><b>Service workers and shop sale workers</b> (e.g. shop sales, cooks, "
                "waiter/bartenders, hairdressers, caretakers, street food/stall salespersons, "
                "childcare workers, teachers aides, healthcare/personal care "
                "assistants etc.) </li>"
                "<LI><b>Large-scale agricultural, forestry and fishery workers</b> </li>"
                "<LI><b>Subsistence farmers, fishers, etc.</b></li>"
                "<LI><b>Craft and related workers</b> (e.g. builders, plumbers, painters, "
                "mechanics, craftsmen, potters, welders, etc.) </li>"
                "<LI><b>Plant and machine operators and assemblers, drivers</b> (e.g. "
                "factory/plant operators, miners, truck/bus drivers, taxi drivers, "
                "train drivers, etc.) </li>"
                "<LI><b>Elementary occupations</b> (e.g. cleaners, farm pickers/labourers, "
                "rickshaw drivers, builder assistants, hawkers, shoe shiners, street car "
                "cleaners, garbage collectors, street sweepers, etc.) </li></ol></div>"
            )
        }
