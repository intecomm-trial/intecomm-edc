from edc_constants.constants import COMPLETE, NEW, NOT_APPLICABLE, OTHER
from intecomm_form_validators import DISSOLVED, IN_FOLLOWUP, RECRUITING

GROUP_STATUS_CHOICES = (
    (NEW, "New"),
    (RECRUITING, "Recruiting"),
    (COMPLETE, "Complete/Ready"),
    (IN_FOLLOWUP, "In followup"),
    (DISSOLVED, "Dissolved"),
)

REFUSAL_REASONS = (
    ("dont_have_time", "I don't have time"),
    ("must_consult_spouse", "I need to consult my spouse"),
    ("dont_want_blood_drawn", "I don't want to have the blood drawn"),
    ("dont_want_to_join", "I don't want to take part"),
    ("need_to_think_about_it", "I haven't had a chance to think about it"),
    (OTHER, "Other, please specify"),
)

RESPONDENT_CHOICES = (
    ("patient", "Patient"),
    ("family", "Family"),
    ("friend", "friend"),
    ("other", "other"),
    (NOT_APPLICABLE, "Not applicable"),
)
