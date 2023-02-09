from django.conf import settings
from edc_model_wrapper import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):
    model: str = settings.SUBJECT_CONSENT_MODEL
    next_url_name = "subject_dashboard_url"
    next_url_attrs = ["subject_identifier"]
    querystring_attrs = [
        "screening_identifier",
        "gender",
        "legal_name",
        "familiar_name",
        "initials",
        "modified",
    ]
