from django.db import models
from django_pandas.managers import DataFrameManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class AppointmentLocationQa(
    UniqueSubjectIdentifierFieldMixin, QaReportModelMixin, BaseUuidModel
):
    """A read-only table of 1120 appointments where
    `appt_type`=`community`.
    """

    report_model = models.CharField(max_length=50, default="meta_reports.appttype")

    visit_code = models.CharField(max_length=50, null=True, blank=True)

    visit_code_sequence = models.IntegerField(default=0)

    objects = DataFrameManager()

    class Meta(UniqueSubjectIdentifierFieldMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Appointment location QA"
        verbose_name_plural = "Appointment location QA"
        default_permissions = qa_reports_permissions
