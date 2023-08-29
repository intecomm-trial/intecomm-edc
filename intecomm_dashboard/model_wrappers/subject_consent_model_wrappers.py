from edc_model_wrapper import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):
    model: str = "intecomm_consent.subjectconsent"
    next_url_name = "subject_dashboard_url"
    next_url_attrs = ["subject_identifier"]
    querystring_attrs = [
        "screening_identifier",
        "gender",
        "modified",
    ]


class SubjectConsentUgModelWrapper(ModelWrapper):
    model: str = "intecomm_consent.subjectconsentug"
    next_url_name = "subject_dashboard_url"
    next_url_attrs = ["subject_identifier"]
    querystring_attrs = [
        "screening_identifier",
        "gender",
        "modified",
    ]
