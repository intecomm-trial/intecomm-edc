from edc_constants.constants import NOT_APPLICABLE, OTHER
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import APPT, APPT_OTHER

FOLLOWUP_REASONS = (
    (APPT, "Study appointment"),
    (APPT_OTHER, "Other routine appointment"),
    (UNSCHEDULED, "Unschedule visit"),
    (OTHER, "Other reason, specify below ..."),
)

INFO_SOURCE = (
    ("hospital_notes", "Hospital notes"),
    ("outpatient_cards", "Outpatient cards"),
    ("patient", "Patient"),
    ("collateral_history", "Collateral History from relative/guardian"),
    (NOT_APPLICABLE, "Not applicable (if missed)"),
    (OTHER, "Other"),
)

VISIT_UNSCHEDULED_REASON = (
    ("patient_unwell_outpatient", "Patient unwell (outpatient)"),
    ("patient_hospitalised", "Patient hospitalised"),
    ("routine_non_study", "Routine appointment (non-study)"),
    ("recurrence_symptoms", "Recurrence of symptoms"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

VISIT_REASON = (
    (SCHEDULED, "Scheduled visit"),
    (UNSCHEDULED, "Unscheduled visit"),
    (MISSED_VISIT, "Missed visit"),
)
