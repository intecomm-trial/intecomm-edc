from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import DurationField as DjangoDurationField
from django.utils.translation import gettext as _
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_model.utils import duration_hm_to_timedelta
from edc_model_fields.fields import (
    CharField2,
    IntegerField2,
    ManyToManyField2,
    OtherCharField,
)

from intecomm_lists.models import Conditions, MoneySources, TravelMethods, VisitReasons

from ...choices import (
    ACCOMPANIED_BY,
    FACILITY_VISIT_ALTERNATIVES,
    FACILITY_VISIT_ALTERNATIVES_NA,
    MED_COLLECTION_LOCATIONS,
    MONEY_SOURCES,
    NOT_COLLECTED_REASONS,
    REFERRAL_FACILITY,
    REFERRAL_TYPE,
    TESTS_NOT_DONE_REASONS,
)
from ...model_mixins import CrfModelMixin
from ..fields import DurationAsStringField, ExpenseField


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

    travel_duration = DurationAsStringField(
        verbose_name="How long did it take you to reach here?",
        null=True,
        blank=False,
        metadata="FTRATIME1",
    )

    travel_tdelta = DjangoDurationField(
        null=True,
        blank=True,
        editable=False,
    )

    travel_cost = ExpenseField(
        verbose_name=_(
            "Thinking about yourself and anyone that accompanied you, "
            "how much was spent on travel from your home to reach here?"
        ),
        null=True,
        blank=False,
        metadata="FTRAVCOST1",
    )

    food_cost = ExpenseField(
        verbose_name=_(
            "Thinking about yourself and anyone that accompanied you, how much did you "
            "have to pay for food, drink or other refreshments during your travel or "
            "during your visit? (e.g. food, drink, etc.)"
        ),
        null=True,
        blank=False,
        metadata="FFOODCOST1",
    )

    care_visit_reason = ManyToManyField2(
        VisitReasons,
        verbose_name=_("What was the reason for today’s visit?"),
        metadata="FMEDCOND1",
    )

    care_visit_reason_other = OtherCharField(metadata="FMEDCONDOTHER1")

    care_visit_cost = ExpenseField(
        verbose_name=_(
            "How much money did you spend on healthworker and consultation "
            "fees during today’s visit?"
        ),
        null=False,
        blank=False,
        metadata="FFEECOST1",
    )

    med_prescribed = CharField2(
        verbose_name=_("Were you prescribed any medicines during today’s visit?"),
        max_length=25,
        choices=YES_NO,
        metadata="FMED1",
    )

    med_conditions = ManyToManyField2(
        Conditions,
        verbose_name=_("What were the medicines were for?"),
        blank=True,
        metadata="FMEDCOND1",
    )

    med_conditions_other = OtherCharField(metadata="FMEDCONDOTHER1")

    med_collected = CharField2(
        verbose_name=_(
            "Did you receive/collect these medicines (whether paid or received for free)?"
        ),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FMEDCOLL1",
    )

    med_not_collected_reason = CharField2(
        verbose_name=_("Why were these medicines not received/collected?"),
        max_length=25,
        choices=NOT_COLLECTED_REASONS(),
        default=NOT_APPLICABLE,
        metadata="FMED1",
    )

    med_not_collected_reason_other = OtherCharField(metadata="FMEDOTHER1")

    med_cost_tot = ExpenseField(
        verbose_name=_("How much was spent on these medicines? "),
        metadata="FMEDCOST1",
    )

    med_cost_hiv = ExpenseField(
        verbose_name=_("How much was spent on HIV medicines? "),
        metadata="FMEDCOSTHIV1",
    )

    med_cost_htn = ExpenseField(
        verbose_name=_("How much was spent on Hypertension medicines? "),
        metadata="FMEDCOSTHTN1",
    )

    med_cost_dm = ExpenseField(
        verbose_name=_("How much was spent on Diabetes medicines? "),
        metadata="FMEDCOSTDM1",
    )

    med_cost_other = ExpenseField(
        verbose_name=_("How much was spent on OTHER medicines? "),
        metadata="FMEDCOSTOTHER1",
    )

    med_collected_location = CharField2(
        verbose_name="Where did you collect the medicines from?",
        max_length=25,
        choices=MED_COLLECTION_LOCATIONS(),
        default=NOT_APPLICABLE,
        metadata="FMEDCOLLECTLOC1",
    )

    med_collected_location_other = OtherCharField(
        metadata="FMEDCOLLECTLOCOTHER1",
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

    tests_cost = ExpenseField(
        verbose_name=_("How much did you spend on these tests?"),
        metadata="FTESTCOST1",
    )

    care_visit_duration = DurationAsStringField(
        verbose_name=_(
            "How much time did you spend during your visit today -- "
            "from arrival to this place until the end of your visit?"
        ),
        blank=False,
        metadata="FFACTIME1",
    )

    care_visit_tdelta = DjangoDurationField(
        null=True,
        blank=True,
        editable=False,
    )

    with_hcw_duration = DurationAsStringField(
        verbose_name=_(
            "How much time did you spend during the consultation "
            "(i.e. time spent with the healthcareworker)?"
        ),
        blank=False,
        metadata="FWORKTIME1",
    )

    with_hcw_tdelta = DjangoDurationField(
        null=True,
        blank=True,
        editable=False,
    )

    missed_activities = CharField2(
        verbose_name=_(
            "If you were not attending the visit today, what would you have been doing?"
        ),
        max_length=25,
        choices=FACILITY_VISIT_ALTERNATIVES(),
        metadata="FACTIVITY1",
    )

    missed_activities_other = OtherCharField(metadata="FMEDOTHER1")

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
        default=NOT_APPLICABLE,
        metadata="FREFTYPE1",
    )

    referral_facility = CharField2(
        verbose_name=_("What type of facility have you been referred to?"),
        max_length=25,
        choices=REFERRAL_FACILITY(),
        default=NOT_APPLICABLE,
        metadata="FREFAC1",
    )

    accompany = CharField2(
        verbose_name="Who accompanied you here today?",
        max_length=25,
        null=True,
        blank=False,
        choices=ACCOMPANIED_BY(),
        metadata="FACMP1",
    )

    accompany_num = IntegerField2(
        verbose_name=_("Number of people who accompanied you here today"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(15)],
        metadata="FACMP1",
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
        choices=FACILITY_VISIT_ALTERNATIVES_NA(),
        default=NOT_APPLICABLE,
        metadata="FACMPACT1",
    )

    accompany_alt_other = OtherCharField(metadata="FACMPACTOTHER")

    money_sources = ManyToManyField2(
        MoneySources,
        verbose_name=_(
            "Thinking about the expenses you have reported for today’s visit, what were "
            "the source(s) of payment for all these expenses?"
        ),
        limit_choices_to={"name__in": [n[0] for n in MONEY_SOURCES if n[0] != NOT_APPLICABLE]},
        help_text="Select up to three sources. If 'other', please specify.",
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
        default=NOT_APPLICABLE,
        metadata="FTODSOURCEMAIN1",
    )

    def save(self, *args, **kwargs):
        if self.travel_duration:
            self.travel_tdelta = duration_hm_to_timedelta(self.travel_duration)
        if self.care_visit_duration:
            self.care_visit_tdelta = duration_hm_to_timedelta(self.care_visit_duration)
        if self.with_hcw_duration:
            self.with_hcw_tdelta = duration_hm_to_timedelta(self.with_hcw_duration)
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Cost of Careseeking: Part A"
        verbose_name_plural = "Cost of Careseeking: Part A"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
