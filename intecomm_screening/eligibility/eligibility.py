from typing import Any

from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from edc_constants.constants import NO, TBD, YES
from edc_utils import get_utcnow

from .eligibility_part_one import EligibilityPartOne
from .eligibility_part_two import EligibilityPartTwo


class SubjectScreeningEligibilityError(Exception):
    pass


def get_eligible_as_word(
    obj=None,
    eligible_part_one=None,
    eligible_part_two=None,
    unsuitable_for_study=None,
    reasons_ineligible=None,
):
    eligible = TBD
    reasons_ineligible = {} if reasons_ineligible is None else reasons_ineligible
    eligible_part_one = obj.eligible_part_one if obj else eligible_part_one
    eligible_part_two = obj.eligible_part_two if obj else eligible_part_two
    unsuitable_for_study = obj.unsuitable_for_study if obj else unsuitable_for_study

    if unsuitable_for_study == YES:
        reasons_ineligible.update(unsuitable_for_study="Subject unsuitable")
        eligible = NO
    elif all(
        [
            eligible_part_one == YES,
            eligible_part_two == YES,
        ]
    ):
        eligible = YES
    elif NO in [eligible_part_one, eligible_part_two]:
        eligible = NO
    elif TBD in [eligible_part_one, eligible_part_two]:
        eligible = TBD
    if eligible == YES and reasons_ineligible:
        raise SubjectScreeningEligibilityError(
            f"Expected reasons_ineligible to be None. Got {reasons_ineligible}."
        )
    return eligible, reasons_ineligible


def get_display_label(obj):
    eligible, _ = get_eligible_as_word(obj)
    if eligible == YES:
        display_label = "ELIGIBLE"
    elif eligible == TBD:
        display_label = "PENDING"
    else:
        display_label = "not eligible"
    return display_label


class IntecommEligibility:
    """A wrapper class for three eligibility classes.

    Determines if a subject is eligible or not.

    Eligibility is assessed in two parts.

    Instantiated in the save() method of the screening proxy models.

    # For example, for part one:
    #
    #     def save(self, *args, **kwargs):
    #         eligibility = Eligibility(self)
    #         try:
    #             eligibility.assess_eligibility_for_part_one()
    #         except EligibilityPartOneError:
    #             pass
    #         eligibility.update_eligibility_fields()
    #         super().save(*args, **kwargs)

    """

    eligibility_values = [YES, NO, TBD]
    default_options = dict(
        eligible_value_default=TBD,
        eligible_values_list=[YES, NO, TBD],
        is_eligible_value=YES,
    )

    def __init__(
        self,
        model_obj: models.Model = None,
        defaults: dict = None,
        update_model=None,
    ):
        self.part_one = None
        self.part_two = None
        self.update_model = True if update_model is None else update_model
        self.eligible = TBD
        self.reasons_ineligible = {}
        self.model_obj = model_obj
        self.default_options = defaults or self.default_options
        self.assess_eligibility_for_all_parts()
        if self.update_model:
            self.update_model_final()

    def __repr__(self: Any) -> str:
        return f"{self.__class__.__name__}()"

    def assess_eligibility_for_all_parts(self: Any):
        eligibility_part_one_cls = EligibilityPartOne
        eligibility_part_two_cls = EligibilityPartTwo
        self.part_one = eligibility_part_one_cls(
            model_obj=self.model_obj,
            update_model=self.update_model,
            **self.default_options,
        )
        self.reasons_ineligible.update(**self.part_one.reasons_ineligible)
        self.part_two = eligibility_part_two_cls(
            model_obj=self.model_obj,
            update_model=self.update_model,
            **self.default_options,
        )
        self.reasons_ineligible.update(**self.part_two.reasons_ineligible)
        self.check_eligibility_values_or_raise()
        opts = dict(
            eligible_part_one=self.part_one.eligible,
            eligible_part_two=self.part_two.eligible,
            reasons_ineligible=self.reasons_ineligible,
            unsuitable_for_study=self.model_obj.unsuitable_for_study,
        )
        self.eligible, self.reasons_ineligible = get_eligible_as_word(**opts)

    def update_model_final(self: Any):
        self.model_obj.reasons_ineligible = "|".join(self.reasons_ineligible)
        self.model_obj.eligible = self.is_eligible
        if self.is_eligible:
            self.model_obj.eligibility_datetime = (
                self.model_obj.part_two_report_datetime or get_utcnow()
            )
        else:
            self.model_obj.eligibility_datetime = None

    @property
    def is_eligible(self: Any) -> bool:
        """Returns True if eligible else False"""
        return True if self.eligible == YES else False

    def check_eligibility_values_or_raise(self: Any):
        for response in [
            self.part_one.eligible,
            self.part_two.eligible,
        ]:
            if response not in self.eligibility_values:
                raise SubjectScreeningEligibilityError(
                    "Invalid value for `eligible`. "
                    f"Expected one of [{self.eligibility_values}]. Got `{response}`."
                )

    @property
    def display_label(self: Any):
        return get_display_label(obj=self.model_obj)

    def eligibility_status(self: Any, add_urls=None):
        if add_urls:
            url_p1 = reverse(
                "intecomm_screening_admin:intecomm_screening_screeningpartone_change",
                args=(self.part_one.model_obj.id,),
            )
            url_p2 = reverse(
                "intecomm_screening_admin:intecomm_screening_screeningparttwo_change",
                args=(self.part_two.model_obj.id,),
            )
            status_str = format_html(
                f'<A href="{url_p1}">P1: {self.part_one.eligible.upper()}</A><BR>'
                f'<A href="{url_p2}">P2: {self.part_two.eligible.upper()}</A><BR>'
            )
        else:
            status_str = (
                f"P1: {self.part_one.eligible.upper()}<BR>"
                f"P2: {self.part_two.eligible.upper()}<BR>"
            )
        display_label = self.display_label
        if "PENDING" in display_label:
            display_label = f'<font color="orange"><B>{display_label}</B></font>'
        return status_str + display_label
