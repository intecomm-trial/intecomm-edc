from django.db import models
from edc_qareports.models import QaReportModelMixin


class SubjectsTransferred(QaReportModelMixin, models.Model):

    consented = models.DateField()
    visit_code = models.CharField(max_length=100)
    last_visit = models.DateField(null=True, blank=True)
    transferred = models.DateField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    offstudy = models.DateField(null=True, blank=True)
    last_seen = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "subjects_transferred_view"
        verbose_name = "Subjects Transferred"
        verbose_name_plural = "Subjects Transferred"
