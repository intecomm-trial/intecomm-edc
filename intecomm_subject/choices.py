from django.utils.translation import gettext_lazy as _
from edc_constants.constants import (
    BOTH,
    DIVORCED,
    DM,
    DONT_KNOW,
    ESTIMATED,
    HIV,
    HTN,
    INPATIENT,
    LAST_WEEK,
    MARRIED,
    MEASURED,
    NEVER,
    NO,
    NOT_APPLICABLE,
    ONGOING,
    OTHER,
    OUTPATIENT,
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
from edc_model_fields.utils import Choices
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)
from edc_visit_tracking.constants import MISSED_VISIT, SCHEDULED, UNSCHEDULED

from .constants import (
    ADULT,
    ALONE,
    CHILD,
    COMMUNITY_CLINIC,
    EXPENSIVE,
    GTE_3HRS,
    HOME_REMEDIES,
    MAIN_EARNER,
    NURSE,
    PAID_WORK,
    PROBLEMATIC,
    SITTING,
    STUDY_VISIT,
    TOO_BUSY,
    UNAVAILABLE,
    UNIMPORTANT,
    UNPAID_WORK,
)

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


TRAVEL_METHODS = Choices(
    ("walking", _("Walking"), 1),
    ("public_transport", _("Public Transport (government bus, etc)")),
    ("hired_transport", _("Hired / shared transport (bus, taxi, boda boda etc)")),
    (
        "own_transport",
        _(
            "Own vehicle (bicycle, animal-drawn cart, motorcycle, scooter, tractor, car, etc)",
        ),
    ),
    (
        "borrowed_transport",
        (
            _(
                "Somebody else’s vehicle (bicycle, animal-drawn cart, "
                "motorcycle, scooter, tractor, car, etc)"
            )
        ),
    ),
    fillmeta=True,
)

VISIT_REASONS = Choices(
    ("routine", "Regular follow-up/check-up", 1),
    ("tests", "Diagnostic tests"),
    ("refill", "Medicines pick-up/refill"),
    ("unwell", "Need treatment/care for illness"),
    (STUDY_VISIT, "Only for study visit"),
    (OTHER, "Other, please specify ..."),
    fillmeta=True,
)


MEDS = Choices(
    (HIV, "HIV", 1),
    (HTN, "Hypertension"),
    (DM, "Diabetes"),
    (OTHER, "Other, please specify ..."),
    fillmeta=True,
)

MED_COLLECTION_LOCATIONS = Choices(
    ("public_pharmacy", "Public pharmacy"),
    ("private_pharmacy", "Private pharmacy"),
    ("club", "Club"),
    (OTHER, "Other, please specify ..."),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)

NOT_COLLECTED_REASONS = Choices(
    ("meds_at_home", "Already had the medicines at home", 1),
    (UNAVAILABLE, "Medicines were not available"),
    (EXPENSIVE, "Medicines were too expensive"),
    (HOME_REMEDIES, "Home remedies are better"),
    (UNIMPORTANT, "Did not think it was important to get these medicines"),
    (TOO_BUSY, "Did not have the time to collect or buy medicines"),
    (PROBLEMATIC, "Taking medicines caused problems"),
    (OTHER, "Other, please specify ..."),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)


TESTS_NOT_DONE_REASONS = Choices(
    (UNAVAILABLE, "Tests were not available and not done", 1),
    (EXPENSIVE, "Tests were too expensive"),
    (UNIMPORTANT, "Did not think it was important to do these tests "),
    (TOO_BUSY, "Did not have the time to do these tests"),
    (OTHER, "Other, please specify ..."),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)

FACILITY_VISIT_ALTERNATIVES = Choices(
    (
        PAID_WORK,
        "Paid work (e.g. full-time employment, small business owners/traders, day jobs, etc.)",
        1,
    ),
    (UNPAID_WORK, "Unpaid work (e.g. subsistence farming, housework etc.)"),
    (OTHER, "Other (specify)"),
    fillmeta=True,
)

FACILITY_VISIT_ALTERNATIVES_NA = Choices(
    (
        PAID_WORK,
        "Paid work (e.g. full-time employment, small business owners/traders, day jobs, etc.)",
        1,
    ),
    (UNPAID_WORK, "Unpaid work (e.g. subsistence farming, housework etc.)"),
    (OTHER, "Other (specify)"),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)

REFERRAL_TYPE = Choices(
    ("inpatient", "Inpatient", 1),
    ("outpatient", "Outpatient (includes laboratory testing)"),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)

REFERRAL_FACILITY = Choices(
    ("public_clinic", "Public facility below tertiary level", 1),
    ("private_clinic", "Private clinic"),
    ("private_dx_facility", "Private diagnostic facility"),
    ("ngo_clinic", "NGO clinic"),
    ("public_hospital", "Public Hospital/tertiary facility"),
    ("private_hospital", "Private hospital"),
    ("pharmacy", "Pharmacy"),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)

_accompany = (
    (ALONE, "No one, I came alone", 1),
    (MAIN_EARNER, "Main household earner"),
    (ADULT, "Other family member/relatives/friends (adults)"),
    (CHILD, "Other family member/relatives/friends (children)"),
    (NOT_APPLICABLE, "Not applicable"),
)
ACCOMPANIED_BY = Choices(*[t for t in _accompany if t[0] != NOT_APPLICABLE], fillmeta=True)

ACCOMPANIED_BY_NA = Choices(*_accompany, fillmeta=True)

_MONEY_SOURCES = (
    ("own_savings", "Own saving (e.g. “loose funds”, bank savings)", 1),
    ("family_gift", "Money received from family members that does not need to be repaid"),
    ("family_loan", "Loan from family member that needs to be repaid"),
    (
        "gift_relative",
        "Money received from relative/neighbour that does not need to be repaid",
    ),
    ("loan_relative", "Loan from relative/neighbour that needs to be repaid"),
    ("loan_money_lender", "Loan from money lender"),
    ("loan_bank", "Loan from another source eg bank"),
    ("community", "Self-help community group"),
    ("national_insurance", "National health insurance"),
    ("private_insurance", "Private health insurance"),
    ("community_insurance", "Community health insurance"),
    ("waiver", "Government waiver"),
    (
        "asset_sale",
        "Sale of assets (property, livestock, jewellery, household goods, etc)",
    ),
    (OTHER, "Other (specified above)"),
    (NOT_APPLICABLE, "Not applicable"),
)
MONEY_SOURCES_NA = Choices(
    *_MONEY_SOURCES,
    fillmeta=True,
)
MONEY_SOURCES = Choices(
    *[t for t in _MONEY_SOURCES if t[0] != NOT_APPLICABLE],
    fillmeta=True,
)


NO_SEEK_REASONS = Choices(
    ("not_necessary", "Did not think it was necessary ", 1),
    ("recovered", "Recovered before I could go "),
    ("home_remedy", "Home remedy given by family member, relatives, neighbours "),
    ("too_expensive", "Too expensive "),
    ("no_time", "Wanted to but could not find time"),
    ("no_transport", "There was no one to take me"),
    ("facility_too_far", "The health facility is too far/ not easy to reach "),
    ("hcw_unavailable", "Health care practitioner mostly unavailable "),
    ("med_problems", "Taking medicines caused problems"),
    ("hcw_confusing", "Do not understand what the healthcare practitioner says "),
    ("hcw_incompetent", "Practitioner is not competent in their work "),
    (OTHER, "Other (specify)"),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)

SEEK_FACILITIES = Choices(
    ("comm_health_centre", "Community health centre/health post", 1),
    ("gov_dispensary", "Government dispensary"),
    ("phc", "Primary health care center (PHC)"),
    ("private_clinic", "Private clinic"),
    ("ngo", "NGO clinic"),
    ("public_hospital", "Public Hospital"),
    ("private_hospital", "Private hospital"),
    ("pharmacy", "Pharmacy"),
    ("hcw_home", "Any healthcare practitioner’s home"),
    (OTHER, "Other (specify)"),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)

SEEKK_CARE_TYPES = Choices(
    (OUTPATIENT, "Outpatient (includes laboratory testing)", 1),
    (INPATIENT, "Inpatient (stayed overnight for 1 or more nights)"),
    (BOTH, "Both"),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)
