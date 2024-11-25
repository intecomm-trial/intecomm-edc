from dateutil.relativedelta import relativedelta
from django.db import models
from django_pandas.managers import DataFrameManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class Diagnoses(UniqueSubjectIdentifierFieldMixin, QaReportModelMixin, BaseUuidModel):
    """A read-only table with details of each participant's diagnoses.

    Run `python manage.py update_diagnoses` to populate.
    """

    report_model = models.CharField(max_length=50, default="meta_reports.diagnoses")

    baseline_date = models.DateField(null=True)

    hiv = models.BooleanField(default=False)
    htn = models.BooleanField(default=False)
    dm = models.BooleanField(default=False)

    hiv_dx_date = models.DateField(null=True)
    htn_dx_date = models.DateField(null=True)
    dm_dx_date = models.DateField(null=True)

    hiv_dx_days = models.IntegerField(
        default=None, null=True, help_text="Number of days relative to baseline"
    )
    dm_dx_days = models.IntegerField(
        default=None, null=True, help_text="Number of days relative to baseline"
    )
    htn_dx_days = models.IntegerField(
        default=None, null=True, help_text="Number of days relative to baseline"
    )

    baseline_182d = models.IntegerField(
        default=0,
        help_text="Number of diagnoses that qualify as baseline (182d before baseline)",
    )

    baseline_6m = models.IntegerField(
        default=0,
        help_text="Number of diagnoses that qualify as baseline (6m before baseline)",
    )

    vl_baseline_value = models.IntegerField(null=True)

    vl_baseline_date = models.DateField(null=True)

    vl_endline_value = models.IntegerField(null=True)

    vl_endline_date = models.DateField(null=True)

    comment = models.TextField(null=True)

    objects = DataFrameManager()

    def save(self, *args, **kwargs):
        self.baseline_6m = 0
        if self.hiv and self.hiv_dx_date + relativedelta(months=6) <= self.baseline_date:
            self.baseline_6m += 1
        if self.htn and self.htn_dx_date + relativedelta(months=6) <= self.baseline_date:
            self.baseline_6m += 1
        if self.dm and self.dm_dx_date + relativedelta(months=6) <= self.baseline_date:
            self.baseline_6m += 1
        cuttoff = -182
        hiv = 1 if self.hiv and self.hiv_dx_days < cuttoff else 0
        htn = 1 if self.htn and self.htn_dx_days < cuttoff else 0
        dm = 1 if self.dm and self.dm_dx_days < cuttoff else 0
        self.baseline_182d = hiv + htn + dm
        super().save(*args, **kwargs)

    class Meta(UniqueSubjectIdentifierFieldMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Current Conditions"
        verbose_name_plural = "Current Conditions"
        default_permissions = qa_reports_permissions
