from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_constants.choices import YES_NO, YES_NO_UNSURE_NA
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import formatted_date, get_utcnow

from ..choices import RESPONDENT_CHOICES
from .patient_log import PatientLog


class Manager(models.Manager):
    """A manager class for Crf models, models that have an FK to
    the visit model.
    """

    use_in_migrations = True

    def get_by_natural_key(self, patient_log):
        return self.get(patient_log=patient_log)


class PatientCall(SiteModelMixin, BaseUuidModel):

    patient_log = models.ForeignKey(PatientLog, on_delete=models.PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)

    answered = models.CharField(max_length=15, choices=YES_NO, null=True, blank=False)

    respondent = models.CharField(
        max_length=15, choices=RESPONDENT_CHOICES, default=NOT_APPLICABLE
    )

    willing_to_attend = models.CharField(
        max_length=15, choices=YES_NO_UNSURE_NA, default=NOT_APPLICABLE
    )

    attend_date = models.DateField(
        verbose_name="When can the patient come to the clinic", null=True, blank=True
    )

    call_again = models.CharField(verbose_name="Call again?", max_length=15, choices=YES_NO)

    comment = EncryptedTextField(verbose_name="Note", null=True, blank=True)

    on_site = CurrentSiteManager()
    objects = Manager()
    history = HistoricalRecords()

    def __str__(self):
        report_dt = formatted_date(self.report_datetime.date())
        call_again = "Do not call" if self.call_again == NO else "Call again"
        if self.willing_to_attend == NO:
            msg = f"{report_dt}: {self.patient_log.name} is NOT willing. {call_again}."
        elif self.willing_to_attend == YES and self.attend_date:
            dt = formatted_date(self.attend_date)
            msg = f"{report_dt}: {self.patient_log.name} is willing to attend on {dt}."
        elif self.call_again == YES:
            msg = (
                f"{report_dt}: {self.patient_log.name} was last called "
                f"{self.report_datetime}. {call_again}."
            )
        else:
            msg = f"{report_dt}: {self.patient_log.name}."
        return msg

    def natural_key(self):
        return (self.patient_log,)

    natural_key.dependencies = [
        "sites.Site",
        "intecomm_screening.patientlog",
    ]

    class Meta:
        verbose_name = "Patient Call"
        verbose_name_plural = "Patient Calls"
        ordering = ["report_datetime"]
