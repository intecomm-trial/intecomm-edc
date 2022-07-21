from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YESDEFAULT_NO
from edc_constants.constants import YES


class PartOneFieldsModelMixin(models.Model):
    screening_consent = models.CharField(
        verbose_name=(
            "Has the subject given his/her verbal consent "
            "to be screened for the INTECOMM trial?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    patient_conditions = models.CharField(
        verbose_name="The participant has at least one of the following conditions: HIV, "
        "diabetes or hypertension?",
        max_length=15,
        null=True,
        choices=YES_NO,
    )

    staying_nearby_6 = models.CharField(
        verbose_name=(
            "Is the patient planning to remain in the catchment area " "for at least 6 months"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    fasted = models.CharField(
        verbose_name="Did the patient come to the clinic fasted?",
        max_length=15,
        null=True,
        choices=YES_NO,
    )

    appt_datetime = models.DateTimeField(
        verbose_name="Appointment date for second stage of screening (P2)",
        null=True,
        blank=True,
        help_text="Leave blank if continuing to the second stage today",
    )

    continue_part_two = models.CharField(
        verbose_name=mark_safe("Continue with <U>part two</U> of the screening process?"),
        max_length=15,
        choices=YESDEFAULT_NO,
        default=YES,
        help_text=mark_safe(
            "<B>Important</B>: This response will be be automatically "
            "set to YES if:<BR><BR>"
            "- the participant meets the eligibility criteria for part one, or;<BR><BR>"
            "- the eligibility criteria for part two is already complete.<BR>"
        ),
    )

    class Meta:
        abstract = True
