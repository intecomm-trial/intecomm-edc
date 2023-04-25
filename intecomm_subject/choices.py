from edc_constants.constants import (
    ESTIMATED,
    MEASURED,
    NEVER,
    NO,
    NOT_APPLICABLE,
    OTHER,
    PATIENT,
    YES,
)
from edc_dx_review.constants import DIET_LIFESTYLE, DRUGS, THIS_CLINIC
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import COMMUNITY_CLINIC, GTE_3HRS, HEALTH_FACILITY, NURSE, SITTING

ALCOHOL_CONSUMPTION = (
    ("occasionally", "Occasionally"),
    ("1_2_per_week", "1-2 times a week"),
    ("3_4_per_week", "3-4 times a week"),
    ("daily", "Daily"),
    (NOT_APPLICABLE, "Not applicable"),
)

CARE_ACCESS = (
    (THIS_CLINIC, "Patient comes to this facility for their care"),
    (OTHER, "Patient goes to a different clinic"),
    (NOT_APPLICABLE, "Not applicable"),
)

CARE_DELIVERY = (
    (HEALTH_FACILITY, "Health facility"),
    (COMMUNITY_CLINIC, "Community clinic"),
    (OTHER, "Other facility, please specify below ..."),
    (NOT_APPLICABLE, "Not applicable"),
)

DISCLOSURE = (
    ("voluntary", "Voluntary disclosure"),
    ("involuntary", "Involuntary disclosure"),
    ("by_others", "Others told them without permission"),
    (NOT_APPLICABLE, "Not applicable"),
)

EDUCATION = (
    ("no_formal_education", "No Formal Education"),
    ("primary", "Up to primary"),
    ("secondary", "Up to secondary / high school"),
    ("post_secondary", "College or similar higher institution"),
    ("tertiary", "university educated"),
)

EMPLOYMENT_STATUS = (
    ("professional", "Professional / office work / business"),
    ("manual_work", "Skilled / Unskilled manual work"),
    ("housewife", "Housewife"),
    ("unemployed", "Not working / seeking work"),
    ("unemployed_not_seeking", "Not working / NOT seeking work"),
    ("retired", "Retired"),
    (OTHER, "Other, please specify"),
)

HOUSEHOLD_YES_NO_CHOICES = (
    (NO, "No"),
    ("yes_spouse", "Yes, my spouse"),
    ("yes_parents", "Yes, one of my parents living with me"),
    ("yes_relative", "Yes, another relative living with me"),
)

HTN_MANAGEMENT = (
    (DRUGS, "Drugs / Medicine"),
    (DIET_LIFESTYLE, "Diet and lifestyle alone"),
)

IMPACT_SEVERITY = (
    ("minor", "Minor"),
    ("moderate", "Moderate"),
    ("major", "Major"),
    (NOT_APPLICABLE, "Not applicable"),
)

IMPACT_STATUS = (
    ("resolved", "Resolved"),
    ("ongoing", "Ongoing"),
    (NOT_APPLICABLE, "Not applicable"),
)

MISSED_PILLS = (
    ("today", "today"),
    ("yesterday", "yesterday"),
    ("earlier_this_week", "earlier this week"),
    ("last_week", "last week"),
    ("lt_month_ago", "less than a month ago"),
    ("gt_month_ago", "more than a month ago"),
    (NEVER, "have never missed taking my study pills"),
)

MARITAL_STATUS = (
    ("married", "Married or living with someone"),
    ("single", "Single"),
    ("divorced", "Divorced"),
    ("widowed", "Widow / Spinster"),
)


# *********************************
ACTIVITY_CHOICES = (
    ("working", "Working"),
    ("studying", "Studying"),
    ("caring_for_children", "Caring for children"),
    ("house_maintenance", "House maintenance"),
    ("nothing", "Nothing"),
    (OTHER, "Other, please specify"),
)

CARD_TYPE_CHOICES = (
    ("paper_based", "Paper-based"),
    ("electronic", "Electronic"),
    ("both", "Both"),
    (NOT_APPLICABLE, "Not Applicable"),
)

CHILDCARE_CHOICES = (
    (NOT_APPLICABLE, "Not applicable"),
    ("working", "Working"),
    ("studying", "Studying"),
    ("caring_for_children", "Caring for children"),
    ("house_maintenance", "House maintenance"),
    ("nothing", "Nothing"),
    (OTHER, "Other, specify"),
)

GLUCOSE_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
    (NOT_APPLICABLE, "Not applicable"),
)

HCF_PRESCRIPTION_COLLECTION_CHOICES = (
    (YES, "Yes"),
    (NO, "No, I buy my own drugs"),
    (NOT_APPLICABLE, "Not applicable"),
)

INFO_SOURCE = (
    ("patient", "Patient"),
    ("patient_and_outpatient", "Patient, hospital notes and/or outpatient card"),
    ("patient_representive", "Patient Representative (e.family member, friend)"),
    ("hospital_notes", "Hospital notes"),
    ("outpatient_cards", "Outpatient cards"),
    ("collateral_history", "Collateral History from relative/guardian"),
    (NOT_APPLICABLE, "Not applicable"),
    (OTHER, "Other"),
)

MISSED_VISIT_CALLER_CHOICES = (
    (NURSE, "Nurse"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

PHYSICAL_ACTIVITY = (
    ("retired", "Retired"),
    (SITTING, "Mostly sitting"),
    ("standing_or_walking", "Mostly standing or walking"),
    ("physical_effort", "Definite physical effort"),
    ("vigorous_physical_activity", "Vigorous physical activity"),
)

PHYSICAL_ACTIVITY_HOURS = (
    ("none", "None"),
    ("lt_1hr", "Some but less than one hour"),
    ("1-3hr", "1 hour but less than 3 hours"),
    (GTE_3HRS, "3 hours or more"),
)


TRANSPORT_CHOICES = (
    ("bus", "Bus"),
    ("train", "Train"),
    ("ambulance", "Ambulance"),
    ("private_taxi", "Private taxi"),
    ("own_bicycle", "Own bicycle"),
    ("hired_motorbike", "Hired motorbike"),
    ("own_car", "Own car"),
    ("own_motorbike", "Own motorbike"),
    ("hired_bicycle", "Hired bicycle"),
    ("foot", "Foot"),
    (OTHER, "Other, specify"),
)

VISIT_UNSCHEDULED_REASON = (
    ("routine_non_study", "Routine appointment (non-study)"),
    ("patient_unwell_outpatient", "Patient unwell"),
    ("drug_refill", "Drug refill only"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

VISIT_REASON = (
    (SCHEDULED, "Scheduled visit (study)"),
    (UNSCHEDULED, "Routine / Unscheduled visit (non-study)"),
    (MISSED_VISIT, "Missed visit"),
)

ESTIMATED_MEASURED_CHOICES = (
    (MEASURED, "Measured"),
    (ESTIMATED, "Estimated"),
    (NOT_APPLICABLE, "Not recorded / Not applicable"),
)

APPT_DATE_INFO_SOURCES = (
    ("health_records", "Health record"),
    (PATIENT, "Patient"),
    ("estimated", "I estimated the date"),
)
