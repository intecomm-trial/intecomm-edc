from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel, OtherCharField

from intecomm_lists.models import DrugPaySources, TransportChoices

from ..choices import ACTIVITY_CHOICES, CHILDCARE_CHOICES
from ..model_mixins import CrfModelMixin


class HealthEconomics(CrfModelMixin, BaseUuidModel):
    occupation = models.CharField(
        verbose_name="What is your occupation/profession?", max_length=50
    )

    education_in_years = models.IntegerField(
        verbose_name="How many years of education did you complete?",
        validators=[MinValueValidator(0), MaxValueValidator(50)],
    )

    education_certificate = models.CharField(
        verbose_name="What is your highest education certificate?",
        max_length=50,
        null=True,
        blank=True,
    )

    primary_school = models.CharField(
        verbose_name="Did you go to primary/elementary school?",
        max_length=15,
        choices=YES_NO_NA,
    )

    primary_school_in_years = models.IntegerField(
        verbose_name="If YES, for how many years",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    secondary_school = models.CharField(
        verbose_name="Did you go to secondary school?", max_length=15, choices=YES_NO_NA
    )

    secondary_school_in_years = models.IntegerField(
        verbose_name="If YES, for how many years",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    higher_education = models.CharField(
        verbose_name="Did you go to higher education?", max_length=15, choices=YES_NO_NA
    )

    higher_education_in_years = models.IntegerField(
        verbose_name="If YES, for how many years",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    welfare = models.CharField(
        verbose_name="Do you receive any welfare or social service support",
        max_length=15,
        choices=YES_NO,
    )

    welfare_other = models.TextField(
        verbose_name="If yes, please explain", max_length=250, null=True, blank=True
    )

    income_per_month = models.IntegerField(
        verbose_name="How much do you earn (take home) per month?",
        help_text="in local currency",
        null=True,
        blank=False,
    )

    household_income_per_month = models.IntegerField(
        verbose_name="What is the total income in your household per month?",
        help_text="in local currency",
        null=True,
        blank=False,
    )

    is_highest_earner = models.CharField(
        verbose_name="Are you the person who earns the highest income in your household?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    highest_earner = models.CharField(
        verbose_name=(
            "If NO, what is the profession of the person who earns the highest income?"
        ),
        max_length=50,
        null=True,
        blank=True,
    )

    # General expenditure
    food_per_month = models.IntegerField(
        verbose_name="How much do you/your family spend on food in a month?",
        help_text="in local currency",
        null=True,
        blank=False,
    )

    accomodation_per_month = models.IntegerField(
        verbose_name=(
            "How much do you/your family spend on rent (or house loan/mortgage) "
            "and utilities in a month?"
        ),
        help_text="in local currency",
        null=True,
        blank=False,
    )

    large_expenditure_year = models.IntegerField(
        verbose_name="How much have you spent on large items in the last year",
        help_text="e.g. furniture, electrical items, cars (in local currency)",
        null=True,
        blank=False,
    )
    #################################################
    # Previous health care expenses: Medications
    received_rx_month = models.CharField(
        verbose_name=(
            "Over the last month, did you get any drugs on "
            "your visit to the health facility?"
        ),
        max_length=15,
        choices=YES_NO,
        help_text="not including today",
    )

    rx_dm_month = models.CharField(
        verbose_name=(
            "Did you receive drugs for raised blood sugar (diabetes) over the last month?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="not including today",
    )
    rx_dm_paid_month = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name="If YES, how were these paid for?",
        blank=True,
    )

    rx_dm_paid_month_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ... (DM)"
    )

    rx_dm_cost_month = models.IntegerField(
        verbose_name="If these drugs were not free, how much did you pay?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    rx_htn_month = models.CharField(
        verbose_name=(
            "Did you receive drugs for raised blood pressure "
            "(hypertension) over the last month?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="not including today",
    )

    rx_htn_paid_month = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name="If YES, how were these paid for?",
        blank=True,
    )

    rx_htn_paid_month_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ...(HTN)"
    )

    rx_htn_cost_month = models.IntegerField(
        verbose_name="If these drugs were not free, how much did you pay?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    rx_hiv_month = models.CharField(
        verbose_name="Did you receive anti-retroviral drugs for HIV over the last month?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="not including today",
    )
    rx_hiv_paid_month = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name="If YES, how were these paid for?",
        max_length=25,
        blank=True,
    )

    rx_hiv_paid_month_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ... (HIV)"
    )

    rx_hiv_cost_month = models.IntegerField(
        verbose_name="If these drugs were not free, how much did you pay?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    rx_other_month = models.CharField(
        verbose_name="Did you receive any 'other' drugs?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    rx_other_paid_month = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name="If YES, received 'other' drugs, how were these paid for?",
        blank=True,
    )

    rx_other_paid_month_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ..."
    )

    rx_other_cost_month = models.IntegerField(
        verbose_name="If not free, how much did you pay for these 'other' drugs?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    #################################################
    # Previous health care expenses: Other

    non_drug_activities_month = models.CharField(
        verbose_name=(
            "Over the last month, did you spend money on other activities (not drugs) "
            "relating to your health?"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    non_drug_activities_detail_month = models.TextField(
        verbose_name="If YES, what was the activity", null=True, blank=True
    )

    non_drug_activities_cost_month = models.IntegerField(
        verbose_name=(
            "If YES, how much was spent on other activities "
            "(not drugs) relating to your health?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In local currency",
        null=True,
        blank=True,
    )

    healthcare_expenditure_total_month = models.IntegerField(
        verbose_name=(
            "How much in total has been spent on your healthcare in the last month?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In local currency",
        null=True,
        blank=False,
    )

    #################################################
    # Loss of Productivity and Earnings
    missed_routine_activities = models.CharField(
        verbose_name=(
            "What would you be doing if you had not come to the health facility today?"
        ),
        max_length=25,
        choices=ACTIVITY_CHOICES,
        null=True,
        blank=False,
    )

    missed_routine_activities_other = models.CharField(
        verbose_name="If OTHER, please specify", max_length=50, null=True, blank=True
    )

    off_work_days = models.DecimalField(
        verbose_name="How much time did you take off work?",
        decimal_places=1,
        max_digits=4,
        help_text="in days. (1,2,3 etc. If half-day 0.5)",
        null=True,
        blank=False,
    )

    travel_time = models.CharField(
        verbose_name="How long did it take you to reach here?",
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
        null=True,
        blank=False,
    )

    hospital_time = models.CharField(
        verbose_name="How much time did you spend at the health care facility?",
        max_length=5,
        help_text="in hours and minutes (format HH:MM)",
        null=True,
        blank=False,
    )

    lost_income = models.CharField(
        verbose_name="Did you lose earnings as a result of coming here today? ",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    lost_income_amount = models.IntegerField(
        verbose_name="If Yes, how much did you lose?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    #################################################
    # Family Loss of Productivity and Earnings
    childcare = models.CharField(
        verbose_name=(
            "Did you ask anyone else, such as your family member/"
            "friend to look after your child/children in order to come here?"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    childcare_source = models.CharField(
        verbose_name=(
            "If Yes, what would they have been doing if they had not stayed to "
            "look after your child or children?"
        ),
        max_length=25,
        choices=CHILDCARE_CHOICES,
        default=NOT_APPLICABLE,
        null=True,
        blank=False,
    )

    childcare_source_other = OtherCharField()

    childcare_source_timeoff = models.DecimalField(
        verbose_name="How much time did a family member or friend take off?",
        decimal_places=1,
        max_digits=4,
        null=True,
        blank=True,
        help_text="in days. (1,2,3 etc. If half-day 0.5)",
    )

    #################################################
    # Current visit: transport and food
    transport = models.ManyToManyField(
        TransportChoices,
        verbose_name="Which form of transport did you take to get to the hospital today?",
        max_length=25,
        blank=False,
    )

    transport_other = OtherCharField(verbose_name="If `other reason`, please specify ...")

    transport_cost = models.IntegerField(
        verbose_name="How much did you spend on transport in total?",
        help_text="Coming to the health care facility going back home. (In local currency)",
        null=True,
        blank=False,
    )

    food_cost = models.IntegerField(
        verbose_name=(
            "How much did you spend on food while "
            "you were at the health care faility today?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In local currency",
        null=True,
        blank=False,
    )

    #######################################################
    # Current Visit: health care expenses
    received_rx_today = models.CharField(
        verbose_name="Did you get any drugs on your visit to the health facility today?",
        max_length=15,
        choices=YES_NO,
    )

    rx_dm_today = models.CharField(
        verbose_name="Did you receive drugs for raised blood sugar (diabetes) today?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )
    rx_dm_paid_today = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name=(
            "If YES, received raised blood sugar (diabetes) drugs, how were these paid for?"
        ),
        blank=True,
    )

    rx_dm_paid_today_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ..."
    )

    rx_dm_cost_today = models.IntegerField(
        verbose_name=(
            "If not free, how much did you pay for raised blood sugar (diabetes) drugs?"
        ),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    rx_htn_today = models.CharField(
        verbose_name="Did you receive raised blood pressure (hypertension) drugs today?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    rx_htn_paid_today = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name=(
            "If YES, received high blood pressure "
            "(Hypertension) drugs, how were these paid for?"
        ),
        blank=True,
    )

    rx_htn_paid_today_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ..."
    )
    rx_htn_cost_today = models.IntegerField(
        verbose_name=(
            "If not free, how much did you pay for high blood pressure (Hypertension) drugs?"
        ),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    rx_hiv_today = models.CharField(
        verbose_name="Did you receive ARVs (HIV) today?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    rx_hiv_paid_today = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name="If YES, received ARV (HIV) drugs, how were these paid for?",
        max_length=25,
        blank=True,
    )

    rx_hiv_paid_today_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ..."
    )

    rx_hiv_cost_today = models.IntegerField(
        verbose_name="If not free, how much did you pay for ARV (HIV) drugs?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )

    rx_other_today = models.CharField(
        verbose_name="Did you receive 'other' drugs today?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    rx_other_paid_today = models.ManyToManyField(
        DrugPaySources,
        related_name="+",
        verbose_name="If YES, received 'other' drugs, how were these paid for?",
        blank=True,
    )

    rx_other_paid_today_other = OtherCharField(
        verbose_name="If `other pay source`, please specify ..."
    )

    rx_other_cost_today = models.IntegerField(
        verbose_name="If not free, how much did you pay for these 'other' drugs?",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="In local currency",
    )
    ########################################################
    # Current Visit: Other expenses

    non_drug_activities_today = models.CharField(
        verbose_name=(
            "Did you spend money on other activities (not drugs) "
            "relating to your health today?"
        ),
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    non_drug_activities_detail_today = models.TextField(
        verbose_name="If YES, what was the activity", null=True, blank=True
    )

    non_drug_activities_cost_today = models.IntegerField(
        verbose_name="If YES, how much did you spend?",
        validators=[MinValueValidator(0)],
        help_text="In local currency",
        null=True,
        blank=True,
    )

    healthcare_expenditure_total_month_today = models.IntegerField(
        verbose_name=(
            "How much in total has been spent on your healthcare in the last month?"
        ),
        validators=[MinValueValidator(0)],
        help_text="In local currency",
        null=True,
        blank=False,
    )

    ########################################################
    # Health care financing
    finance_by_sale = models.CharField(
        verbose_name="Do you sell anything to pay for your visit today?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    finance_by_loan = models.CharField(
        verbose_name="Did you take any loans to pay for your visit?",
        max_length=15,
        choices=YES_NO,
        null=True,
        blank=False,
    )

    health_insurance = models.CharField(
        verbose_name="Do you have private healthcare insurance?",
        max_length=15,
        choices=YES_NO,
    )

    health_insurance_cost = models.IntegerField(
        verbose_name=(
            "If Yes, how much do you pay towards your contributions to "
            "healthcare insurance every month?"
        ),
        null=True,
        blank=True,
        help_text="in local currency",
    )

    patient_club = models.CharField(
        verbose_name="Do you contribute to a patient club?",
        max_length=15,
        choices=YES_NO,
    )

    patient_club_cost = models.IntegerField(
        verbose_name=(
            "If Yes, how much do you pay towards your contributions to "
            "the patient club every month?"
        ),
        null=True,
        blank=True,
        help_text="in local currency",
    )

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Economics"
        verbose_name_plural = "Health Economics"
