from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin

from .view_definition import get_view_definition


class SubjectsTransferred(QaReportModelMixin, DBView):

    consented = models.DateField()
    visit_code = models.CharField(max_length=100)
    last_visit = models.DateField(null=True, blank=True)
    transferred = models.DateField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    offstudy = models.DateField(null=True, blank=True)
    last_seen = models.DateField(null=True, blank=True)

    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "subjects_transferred_view"
        verbose_name = "Subjects Transferred"
        verbose_name_plural = "Subjects Transferred"
