from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import DurationField as DjangoDurationField
from django.utils.translation import gettext as _
from edc_constants.choices import YES_NO, YES_NO_DONT_KNOW_NA, YES_NO_NA
from edc_constants.constants import DM, HIV, HTN, NOT_APPLICABLE, OTHER
from edc_model.models import BaseUuidModel
from edc_model.utils import duration_hm_to_timedelta
from edc_model_fields.fields import (
    CharField2,
    IntegerField2,
    ManyToManyField2,
    OtherCharField,
)

from intecomm_lists.models import Conditions, MoneySources, TravelMethods

from ...choices import (
    ACCOMPANIED_BY_NA,
    FACILITY_VISIT_ALTERNATIVES_NA,
    MONEY_SOURCES_NA,
    NO_SEEK_REASONS,
    NOT_COLLECTED_REASONS,
    SEEK_FACILITIES,
    SEEKK_CARE_TYPES,
    TESTS_NOT_DONE_REASONS,
)
from ...model_mixins import CrfModelMixin
from ..fields import DurationAsStringField, ExpenseField


class CareseekingB(CrfModelMixin, BaseUuidModel):

    needed_care = CharField2(
        verbose_name=_(
            "Other than today’s visit, and thinking about the past 3 months, "
            "did you need to make any routine visits or were you ill or in need of "
            "healthcare at any point for HIV, Hypertension, Diabetes or anything "
            "related to you having these conditions?"
        ),
        max_length=15,
        choices=YES_NO,
        metadata="FILLMONTH1",
    )

    accessed_care = CharField2(
        verbose_name=_(
            "Did you make the visit, seek advice or treatment "
            "(public facility, local pharmacy, traditional doctor etc)?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FSEEK1",
    )

    no_accessed_care = CharField2(
        verbose_name=_("If no, why did you not make the visit, seek advice or treatment?"),
        max_length=25,
        choices=NO_SEEK_REASONS(),
        default=NOT_APPLICABLE,
        help_text="If NO, STOP and SAVE form",
        metadata="FNOSEEK1",
    )

    no_accessed_care_other = OtherCharField(verbose_name="If OTHER reason, please explain ...")

    care_facility = CharField2(
        verbose_name=_("If yes, where did you make the visit, seek advice or treatment?"),
        max_length=25,
        choices=SEEK_FACILITIES(),
        default=NOT_APPLICABLE,
        metadata="FSEEKFAC1",
    )

    care_facility_other = OtherCharField(verbose_name="If OTHER place, please explain ...")

    care_type = CharField2(
        verbose_name=_("If yes, what type of care was this?"),
        max_length=25,
        choices=SEEKK_CARE_TYPES(),
        default=NOT_APPLICABLE,
        metadata="FSEEKTYPE1",
    )

    outpatient_visits = IntegerField2(
        verbose_name=_("If yes and OUTPATIENT or BOTH, how many outpatient visits in total?"),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        metadata="FOUT1",
    )

    travel_method = ManyToManyField2(
        TravelMethods,
        verbose_name=_(
            "Thinking about your last/most recent visit, how did you travel to the visit?"
        ),
        blank=True,
        metadata="FOUTTRA1",
    )

    travel_duration = DurationAsStringField(
        verbose_name=_("How long did it take you to get there?"),
        metadata="FOUTTRATIME1",
    )

    travel_tdelta = DjangoDurationField(
        null=True,
        blank=True,
        editable=False,
    )

    travel_costs = ExpenseField(
        verbose_name=_(
            "Thinking about yourself and anyone that accompanied you, how much was spent "
            "on travel from your home to your last/most recent visit?"
        ),
        metadata="FOUTTRACOST1",
    )

    food_costs = ExpenseField(
        verbose_name=_(
            "Thinking about yourself and anyone that accompanied you, did you have to pay "
            "for food, drink or other refreshments during your travel or during your "
            "last/most recent visit? (e.g. food, drink, etc.)"
        ),
        metadata="FOUTFOODCOST1",
    )

    care_costs = ExpenseField(
        verbose_name=_(
            "How much money did you spend on healthworker and consultation fees "
            "during your last/most recent visit?"
        ),
        metadata="FOUTFEECOST1",
    )

    med_prescribed = CharField2(
        verbose_name=_(
            "Were you prescribed any medicines during your last/most recent visit?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FOUTMED1",
    )

    med_conditions = ManyToManyField2(
        Conditions,
        limit_choices_to={"name__in": [HIV, DM, HTN, OTHER]},
        related_name="%(app_label)s_med_conditions_related",
        related_query_name="%(app_label)s_med_conditions_sources",
        verbose_name=_("What were the medicines were for?"),
        blank=True,
        metadata="FOUTMEDCOND1",
    )

    med_conditions_other = OtherCharField(metadata="FOUTMEDCONDOTHER1")

    med_collected = CharField2(
        verbose_name=_(
            "Did you receive/collect these medicines (whether paid or received for free)?"
        ),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FOUTMEDCOLL1",
    )

    med_not_collected_reason = CharField2(
        verbose_name=_("Why were these medicines not received/collected?"),
        max_length=25,
        choices=NOT_COLLECTED_REASONS(),
        default=NOT_APPLICABLE,
        metadata="FOUTMEDNO1",
    )

    med_not_collected_reason_other = OtherCharField(metadata="FOUTMEDNOOTHER1")

    med_cost_tot = ExpenseField(
        verbose_name=_("How much was spent on these medicines? "),
        metadata="FOUTMEDCOST1",
    )

    tests_requested = CharField2(
        verbose_name=_(
            "Did the healthcare worker request for any tests to be done during "
            "your last/most recent visit?"
        ),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=_("for example, blood pressure, viral load, glucose etc."),
        metadata="FOUTTEST1",
    )

    tests_done = CharField2(
        verbose_name=_("Were the tests performed?"),
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=_("select YES even if done elsewhere / another facility"),
        metadata="FOUTTESTDONE1",
    )

    tests_not_done_reason = CharField2(
        verbose_name=_("Why were the tests not performed?"),
        max_length=25,
        choices=TESTS_NOT_DONE_REASONS(),
        default=NOT_APPLICABLE,
        metadata="FOUTTESTNO1",
    )

    tests_not_done_other = OtherCharField(metadata="FOUTTESTNOOTHER1")

    tests_cost = ExpenseField(
        verbose_name=_("How much did you spend on these tests?"),
        metadata="FOUTTESTCOST1",
    )

    care_visit_duration = DurationAsStringField(
        verbose_name=_(
            "Roughly how much time did you spend during your last/most recent visit?"
        ),
        metadata="FOUTTIME1",
    )

    care_visit_tdelta = DjangoDurationField(
        null=True,
        blank=True,
        editable=False,
    )

    missed_activities = CharField2(
        verbose_name=_("If you were not attending the visit, what would you have been doing?"),
        max_length=25,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        choices=FACILITY_VISIT_ALTERNATIVES_NA(),
        metadata="FOUTACTIVITY1",
    )

    missed_activities_other = OtherCharField(metadata="FMEDOTHER1")

    accompany = CharField2(
        verbose_name="Who accompanied you to your last/most recent visit?",
        max_length=25,
        choices=ACCOMPANIED_BY_NA(),
        default=NOT_APPLICABLE,
        null=True,
        blank=False,
        metadata="FOUTACMP1",
    )

    accompany_num = IntegerField2(
        verbose_name=_("Number of people who accompanied you to your last/most recent visit"),
        null=True,
        blank=True,
        metadata="FOUTACMPNUM1",
    )

    accompany_wait = CharField2(
        verbose_name=_(
            "Did the people accompanying you wait for you during your last/most recent visit?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FOUTACMPWAIT1",
    )

    accompany_alt = CharField2(
        verbose_name=_(
            "If those accompanying you were not attending your last/most recent visit "
            "with you, what would they have been doing?"
        ),
        max_length=25,
        choices=FACILITY_VISIT_ALTERNATIVES_NA(),
        default=NOT_APPLICABLE,
        metadata="FOUTACMPACT1",
    )

    accompany_alt_other = OtherCharField(metadata="FOUTACMPACTOTHER1")

    money_sources = ManyToManyField2(
        MoneySources,
        related_name="%(app_label)s_money_sources_related",
        related_query_name="%(app_label)s_money_sources",
        verbose_name=_(
            "Thinking about the expenses you have reported in the past 3 months, and "
            "excluding today’s visit, what were the source(s) of payment for all "
            "these expenses?  "
        ),
        blank=True,
        help_text="Select up to three sources. If 'other', please specify.",
        metadata="FOUTSOURCE",
    )

    money_sources_other = OtherCharField(
        verbose_name=_("If other 'source of payment', please specify ..."),
        metadata="FOUTSOURCEOTHER",
    )

    money_source_main = CharField2(
        verbose_name=_(
            "Of the various sources that you have just mentioned, "
            "what was the main source of payment?"
        ),
        max_length=25,
        choices=MONEY_SOURCES_NA(),
        default=NOT_APPLICABLE,
        metadata="FOUTSOURCEMAIN1",
    )

    inpatient = CharField2(
        verbose_name="Were you admitted as a INPATIENT?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If NO, STOP and SAVE.",
    )

    inpatient_days = IntegerField2(
        verbose_name=_("How many days in total were you admitted as an INPATIENT?"),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        metadata="FINDAYS1",
    )

    inpatient_reasons = ManyToManyField2(
        Conditions,
        related_name="%(app_label)s_inpatient_reasons_related",
        related_query_name="%(app_label)s_inpatient_reasons_sources",
        verbose_name=_("What was this INPATIENT care for?"),
        blank=True,
        metadata="FINDAYSCOND1",
    )

    inpatient_reasons_other = OtherCharField(
        verbose_name=_("If other 'INPATIENT care' reason, please specify ..."),
        metadata="FINDAYSCOND1",
    )

    inpatient_cost = ExpenseField(
        verbose_name=_("How much was spent in total on your hospital stay?"),
        metadata="FINCOST1",
    )

    inpatient_accompany = CharField2(
        verbose_name=_("Did anyone stay with you at the facility or somewhere else at night?"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=_("for example: guesthouse, hotel, friend or relative’s house"),
        metadata="FINACMP1",
    )

    inpatient_food = CharField2(
        verbose_name=_(
            "When you were first admitted to the facility, was any food and drink bought "
            "for people who accompanied you?"
        ),
        max_length=15,
        choices=YES_NO_DONT_KNOW_NA,
        default=NOT_APPLICABLE,
        metadata="FINFOOD1",
    )

    inpatient_food_cost = ExpenseField(
        verbose_name=_("How much was spent on this food and drink?"),
        metadata="FINFOODCOST1",
    )

    inpatient_nowork_days = IntegerField2(
        verbose_name="When you were ill, how many days were you not able to go to work?",
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        null=True,
        blank=True,
        metadata="FINWRKMISS1",
    )

    inpatient_household_nowork = CharField2(
        verbose_name=_(
            "Apart from the person that accompanied you, was there anyone "
            "else in your household who could not go to work because of your illness?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        metadata="FINOWRKMISS1",
    )

    inpatient_household_nowork_days = IntegerField2(
        verbose_name="How many days did they not go to work?",
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        null=True,
        blank=True,
        metadata="FINODAYSMISS1",
    )

    inpatient_money_sources = ManyToManyField2(
        MoneySources,
        related_name="%(app_label)s_inpatient_money_sources_related",
        related_query_name="%(app_label)s_inpatient_money_sources",
        verbose_name=_(
            "What were the source(s) of payment for all these expenses for your hospital stay?"
        ),
        blank=True,
        help_text="Select up to three sources. If 'other', please specify.",
        metadata="FINSOURCE",
    )

    inpatient_money_sources_other = OtherCharField(
        verbose_name=_("If other 'source of payment', please specify ..."),
        metadata="FINSOURCEOTHER",
    )

    inpatient_money_sources_main = CharField2(
        verbose_name=_(
            "Of the various sources that you have just mentioned, "
            "what was the main source of payment?"
        ),
        max_length=25,
        choices=MONEY_SOURCES_NA(),
        default=NOT_APPLICABLE,
        metadata="FINSOURCEMAIN1",
    )

    inpatient_money_sources_main_other = OtherCharField(
        verbose_name=_("If other main 'source of payment', please specify ..."),
        metadata="FINSOURCEMAIN1OTHER",
    )

    def save(self, *args, **kwargs):
        if self.travel_duration:
            self.travel_tdelta = duration_hm_to_timedelta(self.travel_duration)
        if self.care_visit_duration:
            self.care_visit_tdelta = duration_hm_to_timedelta(self.care_visit_duration)
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Cost of Careseeking: Part B"
        verbose_name_plural = "Cost of Careseeking: Part B"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
