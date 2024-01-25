from django import forms
from django.utils.html import format_html
from edc_consent.utils import get_consent_model_cls
from edc_crf.modelform_mixins import CrfSingletonModelFormMixin
from edc_he.constants import CHF, NHIF
from edc_he.form_validators import HealthEconomicsHouseholdHeadFormValidator
from edc_sites.site import sites

from ...models import HealthEconomicsHouseholdHead
from ..mixins import CrfModelFormMixin


class HealthEconomicsHouseholdHeadForm(
    CrfSingletonModelFormMixin, CrfModelFormMixin, forms.ModelForm
):
    form_validator_cls = HealthEconomicsHouseholdHeadFormValidator

    def clean_hoh_insurance(self):
        hoh_insurance = self.cleaned_data.get("hoh_insurance")
        for obj in hoh_insurance.all():
            uganda_sites = sites.get_by_country(country="uganda")
            if obj.name in [NHIF, CHF] and self.related_visit.site_id in [
                s.site_id for s in uganda_sites
            ]:
                raise forms.ValidationError(
                    f"Invalid select for your country (Uganda). Got `{obj.display_name}`."
                )

        return hoh_insurance

    @property
    def subject_consent(self):
        return get_consent_model_cls().objects.get(
            subject_identifier=self.get_subject_identifier()
        )

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
