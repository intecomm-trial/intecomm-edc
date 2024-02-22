from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_model.validators import hm_validator
from edc_model_fields.fields import (
    CharField2,
    IntegerField2,
    ManyToManyField2,
    OtherCharField,
)

from intecomm_lists.models import (
    Accompanied,
    Conditions,
    MoneySources,
    TravelMethods,
    VisitReasons,
)

from ...choices import (
    FACILITY_VISIT_ALTERNATIVES,
    MONEY_SOURCES,
    NOT_COLLECTED_REASONS,
    REFERRAL_FACILITY,
    REFERRAL_TYPE,
    TESTS_NOT_DONE_REASONS,
)
from ...model_mixins import CrfModelMixin


def convert_to_choices(s: str) -> tuple:
    choices = []
    x = s.split("\n")
    for item in x:
        values = item.split("\t")
        choices.append(tuple(reversed(values)))
    return tuple(choices)


class CareseekingA(CrfModelMixin, BaseUuidModel):
    travel_method = ManyToManyField2(
        TravelMethods,
        verbose_name=_("How did you travel here?"),
        metadata="FTRA1",
    )

    travel_time = CharField2(
        verbose_name="How long did it take you to reach here?",
        max_length=5,
        validators=[hm_validator],
        help_text="in hours and minutes (format HH:MM)",
        metadata="FTRATIME1",
    )

    travel_cost = IntegerField2(
        verbose_name=_(
            "Thinking about yourself and anyone that accompanied you, "
            "how much was spent on travel from your home to reach here?"
        ),
        validators=[MinValueValidator(1), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("in local currency"),
        metadata="FTRAVCOST1",
    )

    food_cost = IntegerField2(
        verbose_name=_(
            "Thinking about yourself and anyone that accompanied you, how much did you "
            "have to pay for food, drink or other refreshments during your travel or "
            "during your visit? (e.g. food, drink, etc.)"
        ),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("in local currency"),
        metadata="FFOODCOST1",
    )

    visit_reason = ManyToManyField2(
        VisitReasons,
        verbose_name=_("What was the reason for today’s visit?"),
        metadata="FMEDCOND1",
    )

    visit_cost = IntegerField2(
        verbose_name=_(
            "How much money did you spend on healthworker and consultation "
            "fees during this visit?"
        ),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        help_text=_("in local currency"),
        metadata="FFEECOST1",
    )

    med_prescribed = CharField2(
        verbose_name=_("Were you prescribed any medicines during this visit?"),
        max_length=25,
        choices=YES_NO,
        metadata="FMED1",
    )

    med_conditions = ManyToManyField2(
        Conditions,
        verbose_name=_("What were the medicines were for?"),
        metadata="FMEDCOND1",
    )

    med_conditions_other = OtherCharField(metadata="FMEDCONDOTHER1")

    med_collected = CharField2(
        verbose_name=_(
            "Did you receive/collect these medicines (whether paid or received for free)?"
        ),
        max_length=25,
        choices=YES_NO,
        metadata="FMEDCOLL1",
    )

    med_not_collected_reason = CharField2(
        verbose_name=_("Why were these medicines not received/collected?"),
        max_length=25,
        choices=NOT_COLLECTED_REASONS(),
        metadata="FMED1",
    )

    med_not_collected_reason_other = OtherCharField(metadata="FMEDOTHER1")

    med_cost_tot = IntegerField2(
        verbose_name=_("How much was spent on these medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        help_text=_("in local currency"),
        metadata="FMEDCOST1",
    )

    med_cost_hiv = IntegerField2(
        verbose_name=_("How much was spent on HIV medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. In local currency"),
        metadata="FMEDCOSTHIV1",
    )

    med_cost_htn = IntegerField2(
        verbose_name=_("How much was spent on Hypertension medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. In local currency"),
        metadata="FMEDCOSTHTN1",
    )

    med_cost_dm = IntegerField2(
        verbose_name=_("How much was spent on Diabetes medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. In local currency"),
        metadata="FMEDCOSTDM1",
    )

    med_cost_other = IntegerField2(
        verbose_name=_("How much was spent on OTHER medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. In local currency"),
        metadata="FMEDCOSTOTHER1",
    )

    tests_requested = CharField2(
        verbose_name=_(
            "Did the healthcare worker request for any tests to be done during this visit?"
        ),
        max_length=25,
        choices=YES_NO,
        metadata="FTEST1",
    )

    tests_done = CharField2(
        verbose_name=_("Were the tests performed?"),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FTESTDONE1",
    )

    tests_not_done_reason = CharField2(
        verbose_name=_("Why were the tests not performed?"),
        max_length=25,
        choices=TESTS_NOT_DONE_REASONS(),
        default=NOT_APPLICABLE,
        metadata="FTESTNO1",
    )

    tests_not_done_other = OtherCharField(metadata="FTESTNOOTHER1")

    tests_cost = IntegerField2(
        verbose_name=_("How much did you spend on these tests?"),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        help_text=_("in local currency"),
        metadata="FTESTCOST1",
    )

    visit_duration = CharField2(
        verbose_name=_(
            "How much time did you spend during your visit today -- "
            "from arrival to this place until the end of your visit?"
        ),
        max_length=5,
        validators=[hm_validator],
        help_text="in hours and minutes (format HH:MM)",
        metadata="FFACTIME1",
    )

    wait_duration = CharField2(
        verbose_name=_("How much time did you spend waiting?"),
        max_length=5,
        validators=[hm_validator],
        help_text="in hours and minutes (format HH:MM)",
        metadata="FWAITIME1",
    )

    with_hcw_duration = CharField2(
        verbose_name=_("How much time did you spend with the healthcare worker?"),
        max_length=5,
        validators=[hm_validator],
        help_text="in hours and minutes (format HH:MM)",
        metadata="FWORKTIME1",
    )

    missed_activities = CharField2(
        verbose_name=_(
            "If you were not attending the visit today, what would you have been doing?"
        ),
        max_length=25,
        choices=FACILITY_VISIT_ALTERNATIVES(),
        metadata="FACTIVITY1",
    )

    visit_lost_income = IntegerField2(
        verbose_name=_("How much would you have made in cash or in-kind for a day’s work?"),
        validators=[MinValueValidator(0), MaxValueValidator(9999999999)],
        null=True,
        blank=True,
        help_text=_(
            "In local currency. Ask for cash value or equivalent cash value for in-kind"
        ),
        metadata="FPAID1",
    )

    referral = CharField2(
        verbose_name=_(
            "As a result of your visit today, have you been referred for further care?"
        ),
        max_length=15,
        choices=YES_NO,
        metadata="FREFER1",
    )

    referral_type = CharField2(
        verbose_name=_("Is this for inpatient or outpatient care?"),
        max_length=25,
        choices=REFERRAL_TYPE(),
        metadata="FREFTYPE1",
    )

    referral_facility = CharField2(
        verbose_name=_("What type of facility have you been referred to?"),
        max_length=25,
        choices=REFERRAL_FACILITY(),
        metadata="FREFAC1",
    )

    accompany = ManyToManyField2(
        Accompanied,
        verbose_name="Who accompanied you here today?",
        metadata="FACMP1",
    )

    accompany_num = IntegerField2(
        verbose_name=_("Number of people who accompanied you here today"), metadata="FACMP1"
    )

    accompany_wait = CharField2(
        verbose_name="Did the people accompanying you wait for you during the visit?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FACMPWAIT1",
    )

    accompany_alt = CharField2(
        verbose_name=(
            "If those accompanying you were not attending the visit with you today, "
            "what would they have been doing?"
        ),
        max_length=25,
        choices=FACILITY_VISIT_ALTERNATIVES(),
        null=True,
        blank=True,
        metadata="FACMPACT1",
    )

    accompany_lost_income = IntegerField2(
        verbose_name=_("How much would they have made in cash or in-kind for a day’s work?"),
        validators=[MinValueValidator(0), MaxValueValidator(9999999999)],
        null=True,
        blank=True,
        help_text=_(
            "In local currency. Ask for cash value or equivalent cash value for in-kind"
        ),
        metadata="FACMP1",
    )

    money_sources = ManyToManyField2(
        MoneySources,
        verbose_name=_(
            "Thinking about the expenses you have reported for today’s visit, what were "
            "the source(s) of payment for all these expenses?"
        ),
        help_text="Select up to three sources. If ‘other’, please specify.",
        metadata="FTODSOURCE",
    )

    money_sources_other = OtherCharField(
        verbose_name=_("If other 'source of payment', please specify ..."),
        metadata="FTODSOURCEOTHER",
    )

    money_source_main = CharField2(
        verbose_name=_(
            "Of the various sources that you have just mentioned, "
            "what was the main source of payment?"
        ),
        max_length=25,
        choices=MONEY_SOURCES(),
        metadata="FTODSOURCEMAIN1",
    )

    money_source_main_other = OtherCharField(
        verbose_name=_("If other main 'source of payment', please specify ...")
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Cost of Careseeking: Part A"
        verbose_name_plural = "Cost of Careseeking: Part A"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
