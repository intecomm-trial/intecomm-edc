from edc_constants.constants import NEVER, NO, NOT_APPLICABLE, OTHER, YES
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import (
    COMMUNITY_CLINIC,
    DIET_LIFESTYLE,
    DRUGS,
    GTE_3HRS,
    HEALTH_FACILITY,
    INSULIN,
    NURSE,
    SITTING,
    THIS_CLINIC,
)

ALCOHOL_CONSUMPTION = (
    ("ocassionally", "Ocassionally"),
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

DM_MANAGEMENT = (
    (INSULIN, "Insulin injections"),
    (DRUGS, "Oral drugs"),
    (DIET_LIFESTYLE, "Diet and lifestyle alone"),
)

EDUCATION = (
    ("no_formal_education", "No Formal Education"),
    ("primary", "Up to primary"),
    ("secondary", "Up to secondary / high school"),
    ("tertiary", "university educated"),
)

EMPLOYMENT_STATUS = (
    ("professional", "Professional / office work / business"),
    ("manual_work", "Skilled / Unskilled manual work"),
    ("housewife", "Housewife"),
    ("unemployed", "Not working / seeking work"),
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

PAYEE_CHOICES = (
    ("own_cash", "Own cash"),
    ("insurance", "Insurance"),
    ("relative", "Relative of others paying"),
    ("free", "Free drugs from the pharmacy"),
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
