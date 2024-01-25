from django.db import models
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField
from edc_constants.choices import YES_NO, YES_NO_UNSURE_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import HistoricalRecords, OtherCharField
from edc_model.validators.phone import phone_number
from edc_sites.managers import CurrentSiteManager
from edc_utils import get_utcnow

from ..choices import RESPONDENT_CHOICES


class Manager(models.Manager):
    """A manager class for Crf models, models that have an FK to
    the visit model.
    """

    use_in_migrations = True

    def get_by_natural_key(self, patient_log):
        return self.get(patient_log=patient_log)


class PatientCallModelMixin(models.Model):
    report_datetime = models.DateTimeField(default=get_utcnow, db_index=True)

    contact_number = EncryptedCharField(blank=False, validators=[phone_number])

    alt_contact_number = EncryptedCharField(null=True, blank=True, validators=[phone_number])

    answered = models.CharField(max_length=15, choices=YES_NO, null=True, blank=False)

    respondent = models.CharField(
        max_length=15, choices=RESPONDENT_CHOICES, default=NOT_APPLICABLE
    )

    survival_status = models.CharField(
        verbose_name="Is the participant known to be alive",
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE,
    )

    catchment_area = models.CharField(
        verbose_name="Does the participant still reside within the catchment area",
        max_length=15,
        choices=YES_NO_UNSURE_NA,
        default=NOT_APPLICABLE,
    )

    last_appt_date = models.DateField(
        verbose_name="When did the patient last seek care",
        null=True,
        blank=True,
        help_text="This may be helpful when updating health records",
    )

    last_attend_clinic = models.CharField(
        verbose_name="Where did the patient last seek care",
        max_length=25,
        # choices=(),
        null=True,
        blank=True,
        help_text="This may be helpful when updating health records",
    )

    last_attend_clinic_other = OtherCharField()

    next_appt_date = models.DateField(
        verbose_name="When will the patient next attend", null=True, blank=True
    )

    call_again = models.CharField(
        verbose_name="May we call again?", max_length=15, choices=YES_NO
    )

    comment = EncryptedTextField(verbose_name="Note", null=True, blank=True)

    objects = Manager()
    on_site = CurrentSiteManager()
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
