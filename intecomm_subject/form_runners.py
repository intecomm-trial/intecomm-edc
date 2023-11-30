from edc_form_runners.decorators import register
from edc_form_runners.form_runner import FormRunner


@register()
class HtnMedicationAdherenceFormRunner(FormRunner):
    model_name = "intecomm_subject.htnmedicationadherence"
    exclude_formfields = ["pill_count"]


@register()
class DmMedicationAdherenceFormRunner(FormRunner):
    model_name = "intecomm_subject.dmmedicationadherence"
    exclude_formfields = ["pill_count"]


@register()
class HivMedicationAdherenceFormRunner(FormRunner):
    model_name = "intecomm_subject.hivmedicationadherence"
    exclude_formfields = ["pill_count"]


@register()
class SubjectVisitFormRunner(FormRunner):
    model_name = "intecomm_subject.subjectvisit"
    exclude_formfields = ["study_status"]


@register()
class SubjectRequisitionFormRunner(FormRunner):
    model_name = "intecomm_subject.subjectrequisition"
    exclude_formfields = ["clinic_verified", "clinic_verified_datetime"]


@register()
class HealthEconomicsAssetsFormRunner(FormRunner):
    model_name = "intecomm_subject.healtheconomicsassets"
    exclude_formfields = ["window_screen_type"]
