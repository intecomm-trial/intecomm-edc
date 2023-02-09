from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.validators import date_not_future


class ClinicalReviewModelMixin(models.Model):
    def get_best_hiv_test_date(self):
        return self.hiv_test_date or self.hiv_test_estimated_datetime

    def get_best_dm_test_date(self):
        self.dm_test_date or self.dm_test_estimated_datetime

    def get_best_htn_test_date(self):
        self.htn_test_date or self.htn_test_estimated_datetime

    @property
    def diagnoses(self):
        return dict(hiv=self.hiv_dx, htn=self.htn_dx, dm=self.dm_dx)

    @property
    def diagnoses_labels(self):
        return dict(hiv="HIV", htn="Hypertension", dm="Diabetes")

    class Meta:
        abstract = True


class ClinicalReviewBaselineHivModelMixin(models.Model):
    hiv_test = models.CharField(
        verbose_name="Has the patient ever tested for HIV infection?",
        max_length=15,
        choices=YES_NO,
    )

    hiv_test_ago = edc_models.DurationYMDField(
        verbose_name="How long ago was the patient's most recent HIV test?",
        null=True,
        blank=True,
        help_text="If positive, most recent HIV(+) test",
    )

    hiv_test_estimated_datetime = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="calculated by the EDC using `hiv_test_ago`",
    )

    hiv_test_date = models.DateField(
        verbose_name="Date of patient's most recent HIV test?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    hiv_dx = models.CharField(
        verbose_name="Has the patient ever tested positive for HIV infection?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If yes, complete form `HIV Initial Review`",
    )

    def save(self, *args, **kwargs):
        if self.hiv_test_ago:
            self.hiv_test_estimated_datetime = edc_models.duration_to_date(
                self.hiv_test_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ClinicalReviewBaselineHtnModelMixin(models.Model):
    htn_test = models.CharField(
        verbose_name="Has the patient ever tested for Hypertension?",
        max_length=15,
        choices=YES_NO,
    )

    htn_test_ago = edc_models.DurationYMDField(
        verbose_name="If Yes, how long ago was the patient tested for Hypertension?",
        null=True,
        blank=True,
    )

    htn_test_estimated_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="calculated by the EDC using `htn_test_ago`",
    )

    htn_test_date = models.DateField(
        verbose_name="Date of patient's most recent Hypertension test?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    htn_dx = models.CharField(
        verbose_name="Has the patient ever been diagnosed with Hypertension",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If yes, complete form `Hypertension Initial Review`",
    )

    def save(self, *args, **kwargs):
        if self.htn_test_ago:
            self.htn_test_estimated_datetime = edc_models.duration_to_date(
                self.htn_test_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ClinicalReviewBaselineDmModelMixin(models.Model):
    dm_test = models.CharField(
        verbose_name="Has the patient ever tested for Diabetes?",
        max_length=15,
        choices=YES_NO,
    )

    dm_test_ago = edc_models.DurationYMDField(
        verbose_name="If Yes, how long ago was the patient tested for Diabetes?",
        null=True,
        blank=True,
    )

    dm_test_estimated_datetime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="calculated by the EDC using `dm_test_ago`",
    )

    dm_test_date = models.DateField(
        verbose_name="Date of patient's most recent Diabetes test?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    dm_dx = models.CharField(
        verbose_name="Have you ever been diagnosed with Diabetes",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If yes, complete form `Diabetes Initial Review`",
    )

    def save(self, *args, **kwargs):
        if self.dm_test_ago:
            self.dm_test_estimated_datetime = edc_models.duration_to_date(
                self.dm_test_ago, self.report_datetime
            )
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
