from django.utils.translation import gettext_lazy as _
from edc_constants.constants import (
    DIVORCED,
    DONT_KNOW,
    ESTIMATED,
    LAST_WEEK,
    MARRIED,
    MEASURED,
    NEVER,
    NO,
    NOT_APPLICABLE,
    ONGOING,
    OTHER,
    PATIENT,
    RESOLVED,
    SINGLE,
    TODAY,
    WIDOWED,
    YES,
    YESTERDAY,
)
from edc_dx_review.constants import DIET_LIFESTYLE, DRUGS, THIS_CLINIC
from edc_facility.constants import HEALTH_FACILITY
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import COMMUNITY_CLINIC, GTE_3HRS, NURSE, SITTING

ALCOHOL_CONSUMPTION = (
    ("occasionally", _("Occasionally")),
    ("1_2_per_week", _("%(freq)s times a week") % {"freq": "1-2"}),
    ("3_4_per_week", _("%(freq)s times a week") % {"freq": "3-4"}),
    ("daily", _("Daily")),
    (NOT_APPLICABLE, _("Not applicable")),
)

CARE_ACCESS = (
    (THIS_CLINIC, _("Patient comes to this facility for their care")),
    (OTHER, _("Patient goes to a different clinic")),
    (NOT_APPLICABLE, _("Not applicable")),
)

CARE_DELIVERY = (
    (HEALTH_FACILITY, _("Health facility")),
    (COMMUNITY_CLINIC, _("Community clinic")),
    (OTHER, _("Other facility, please specify below ...")),
    (NOT_APPLICABLE, _("Not applicable")),
)

DISCLOSURE = (
    ("voluntary", _("Voluntary disclosure")),
    ("involuntary", _("Involuntary disclosure")),
    ("by_others", _("Others told them without permission")),
    (NOT_APPLICABLE, _("Not applicable")),
)

EDUCATION = (
    ("no_formal_education", _("No Formal Education")),
    ("primary", _("Up to primary")),
    ("secondary", _("Up to secondary / high school")),
    ("post_secondary", _("College or similar higher institution")),
    ("tertiary", _("university educated")),
)

EMPLOYMENT_STATUS = (
    ("professional", _("Professional / office work / business")),
    ("manual_work", _("Skilled / Unskilled manual work")),
    ("housewife", _("Housewife")),
    ("unemployed", _("Not working / seeking work")),
    ("unemployed_not_seeking", _("Not working / NOT seeking work")),
    ("retired", _("Retired")),
    (OTHER, _("Other, please specify")),
)

HOUSEHOLD_YES_NO_CHOICES = (
    (NO, _("No")),
    ("yes_spouse", _("Yes, my spouse")),
    ("yes_parents", _("Yes, one of my parents living with me")),
    ("yes_relative", _("Yes, another relative living with me")),
    (DONT_KNOW, _("Don't know")),
)

HTN_MANAGEMENT = (
    (DRUGS, _("Drugs / Medicine")),
    (DIET_LIFESTYLE, _("Diet and lifestyle alone")),
)

IMPACT_SEVERITY = (
    ("minor", _("Minor")),
    ("moderate", _("Moderate")),
    ("major", _("Major")),
    (NOT_APPLICABLE, _("Not applicable")),
)

IMPACT_STATUS = (
    (RESOLVED, _("Resolved")),
    (ONGOING, _("Ongoing")),
    (NOT_APPLICABLE, _("Not applicable")),
)

MISSED_PILLS = (
    (TODAY, _("today")),
    (YESTERDAY, _("yesterday")),
    ("earlier_this_week", _("earlier this week")),
    (LAST_WEEK, _("last week")),
    ("lt_month_ago", _("less than a month ago")),
    # ("gt_month_ago", _("more than a month ago")),
    (NEVER, _("have never missed taking my medications")),
)

MARITAL_STATUS = (
    (MARRIED, _("Married or living with someone")),
    (SINGLE, _("Single")),
    (DIVORCED, _("Divorced")),
    (WIDOWED, _("Widow / Spinster")),
)


# *********************************
ACTIVITY_CHOICES = (
    ("working", _("Working")),
    ("studying", _("Studying")),
    ("caring_for_children", _("Caring for children")),
    ("house_maintenance", _("House maintenance")),
    ("nothing", _("Nothing")),
    (OTHER, _("Other, please specify")),
)

CARD_TYPE_CHOICES = (
    ("paper_based", _("Paper-based")),
    ("electronic", _("Electronic")),
    ("both", _("Both")),
    (NOT_APPLICABLE, _("Not Applicable")),
)

CHILDCARE_CHOICES = (
    (NOT_APPLICABLE, _("Not applicable")),
    ("working", _("Working")),
    ("studying", _("Studying")),
    ("caring_for_children", _("Caring for children")),
    ("house_maintenance", _("House maintenance")),
    ("nothing", _("Nothing")),
    (OTHER, _("Other, specify")),
)

GLUCOSE_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
    (NOT_APPLICABLE, _("Not applicable")),
)

HCF_PRESCRIPTION_COLLECTION_CHOICES = (
    (YES, _("Yes")),
    (NO, _("No, I buy my own drugs")),
    (NOT_APPLICABLE, _("Not applicable")),
)

INFO_SOURCE = (
    ("patient", _("Patient")),
    ("patient_and_outpatient", _("Patient, hospital notes and/or outpatient card")),
    ("patient_representive", _("Patient Representative (e.family member, friend)")),
    ("hospital_notes", _("Hospital notes")),
    ("outpatient_cards", _("Outpatient cards")),
    ("collateral_history", _("Collateral History from relative/guardian")),
    (NOT_APPLICABLE, _("Not applicable")),
    (OTHER, _("Other")),
)

MEDS_NOT_TAKEN_REASON = (
    (NOT_APPLICABLE, _("Not applicable")),
    (OTHER, _("Other, specify below ...")),
)

MISSED_VISIT_CALLER_CHOICES = (
    (NURSE, _("Nurse")),
    (OTHER, _("Other")),
    (NOT_APPLICABLE, _("Not applicable")),
)


PHYSICAL_ACTIVITY = (
    ("retired", _("Retired")),
    (SITTING, _("Mostly sitting")),
    ("standing_or_walking", _("Mostly standing or walking")),
    ("physical_effort", _("Definite physical effort")),
    ("vigorous_physical_activity", _("Vigorous physical activity")),
)

PHYSICAL_ACTIVITY_HOURS = (
    ("none", _("None")),
    ("lt_1hr", _("Some but less than one hour")),
    ("1-3hr", _("1 hour but less than 3 hours")),
    (GTE_3HRS, _("3 hours or more")),
)


TRANSPORT_CHOICES = (
    ("bus", _("Bus")),
    ("train", _("Train")),
    ("ambulance", _("Ambulance")),
    ("private_taxi", _("Private taxi")),
    ("own_bicycle", _("Own bicycle")),
    ("hired_motorbike", _("Hired motorbike")),
    ("own_car", _("Own car")),
    ("own_motorbike", _("Own motorbike")),
    ("hired_bicycle", _("Hired bicycle")),
    ("foot", _("Foot")),
    (OTHER, _("Other, specify")),
)

VISIT_UNSCHEDULED_REASON = (
    ("routine_non_study", _("Routine appointment (non-study)")),
    ("patient_unwell_outpatient", _("Patient unwell")),
    ("drug_refill", _("Drug refill only")),
    (OTHER, _("Other")),
    (NOT_APPLICABLE, _("Not applicable")),
)

VISIT_REASON = (
    (SCHEDULED, _("Scheduled visit (study)")),
    (UNSCHEDULED, _("Routine / Unscheduled visit (non-study)")),
    (MISSED_VISIT, _("Missed visit")),
)

ESTIMATED_MEASURED_CHOICES = (
    (MEASURED, _("Measured")),
    (ESTIMATED, _("Estimated")),
    (NOT_APPLICABLE, _("Not recorded / Not applicable")),
)

APPT_DATE_INFO_SOURCES = (
    ("health_records", _("Health record")),
    (PATIENT, _("Patient")),
    ("estimated", _("I estimated the date")),
)
