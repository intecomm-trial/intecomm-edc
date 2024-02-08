from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import DM, HIV, HTN, NOT_APPLICABLE, OTHER
from edc_model.models import BaseUuidModel
from edc_model.validators import hm_validator
from edc_model_fields.fields import (
    CharField2,
    IntegerField2,
    ManyToManyField2,
    OtherCharField,
)
from edc_model_fields.utils import Choices

from intecomm_lists.models import Conditions

from ..constants import (
    EXPENSIVE,
    HOME_REMEDIES,
    PROBLEMATIC,
    TOO_BUSY,
    UNAVAILABLE,
    UNIMPORTANT,
)
from ..model_mixins import CrfModelMixin

TRAVEL_OPTIONS = Choices(
    ("walking", _("Walking"), 1),
    ("public_transport", _("Public Transport (government bus, etc)")),
    ("hired_transport", _("Hired / shared transport (bus, taxi etc)")),
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
    ("study_visit", "Only for study visit"),
    fillmeta=True,
)


MEDS = Choices(
    (HIV, "HIV"),
    (HTN, "Hypertension"),
    (DM, "Diabetes"),
    (OTHER, "Other, please specify ..."),
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
    fillmeta=True,
)


TESTS_NOT_DONE_REASONS = Choices(
    (UNAVAILABLE, "Tests were not available", 1),
    (EXPENSIVE, "Tests were too expensive"),
    (UNIMPORTANT, "Did not think it was important to do these tests "),
    (TOO_BUSY, "Did not have the time to do these tests"),
    (OTHER, "Other, please specify ..."),
    (NOT_APPLICABLE, "Not applicable"),
    fillmeta=True,
)


def convert_to_choices(s: str) -> tuple:
    choices = []
    x = s.split("\n")
    for item in x:
        choices.append(tuple(item.split("\t")))
    return tuple(choices)


class CareseekingCost(CrfModelMixin, BaseUuidModel):
    travel_method = CharField2(
        verbose_name=_("How did you travel here?"),
        max_length=25,
        choices=TRAVEL_OPTIONS,
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
        help_text=_("amount in local currency"),
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
        help_text=_("amount in local currency"),
        metadata="FFOODCOST1",
    )

    visit_reason = CharField2(
        verbose_name=_("What was the reason for today’s visit?"),
        max_length=25,
        choices=VISIT_REASONS,
        metadata="FMEDCOND1",
    )

    visit_cost = IntegerField2(
        verbose_name=_(
            "How much money did you spend on healthworker and consultation "
            "fees during this visit?"
        ),
        max_length=25,
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        help_text=_("amount in local currency"),
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
        choices=NOT_COLLECTED_REASONS,
        metadata="FMED1",
    )

    med_not_collected_other = OtherCharField(metadata="FMEDOTHER1")

    med_cost_tot = IntegerField2(
        verbose_name=_("How much was spent on these medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        help_text=_("amount in local currency"),
        metadata="FMEDCOST1",
    )

    med_cost_hiv = IntegerField2(
        verbose_name=_("How much was spent on HIV medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. amount in local currency"),
        metadata="FMEDCOSTHIV1",
    )

    med_cost_htn = IntegerField2(
        verbose_name=_("How much was spent on Hypertension medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. amount in local currency"),
        metadata="FMEDCOSTHTN1",
    )

    med_cost_dm = IntegerField2(
        verbose_name=_("How much was spent on Diabetes medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. amount in local currency"),
        metadata="FMEDCOSTDM1",
    )

    med_cost_other = IntegerField2(
        verbose_name=_("How much was spent on OTHER medicines? "),
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        null=True,
        blank=True,
        help_text=_("Leave blank if not applicable. amount in local currency"),
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
        choices=TESTS_NOT_DONE_REASONS,
        default=NOT_APPLICABLE,
        metadata="FTESTNO1",
    )

    tests_not_done_other = OtherCharField(metadata="FTESTNOOTHER1")

    tests_cost = IntegerField2(
        verbose_name=_("How much money did you spend on these tests?"),
        max_length=25,
        validators=[MinValueValidator(0), MaxValueValidator(9999999)],
        help_text=_("amount in local currency"),
        metadata="FTESTCOST1",
    )

    facility_time = CharField2(
        verbose_name=_(
            "How much time did you spend during your visit today -- "
            "from arrival to this place until the end of your visit?"
        ),
        max_length=5,
        validators=[hm_validator],
        help_text="in hours and minutes (format HH:MM)",
        metadata="FFACTIME1",
    )

    wait_time = CharField2(
        verbose_name=_("How much time did you spend waiting?"),
        max_length=5,
        validators=[hm_validator],
        help_text="in hours and minutes (format HH:MM)",
        metadata="FWAITIME1",
    )

    hworker_time = CharField2(
        verbose_name=_("How much time did you spend with the healthcare worker?"),
        max_length=5,
        validators=[hm_validator],
        help_text="in hours and minutes (format HH:MM)",
        metadata="FWORKTIME1",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Cost of Careseeking"
        verbose_name_plural = "Cost of Careseeking"
        indexes = CrfModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
