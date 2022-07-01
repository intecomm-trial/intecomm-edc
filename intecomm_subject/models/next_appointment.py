from django.db import models
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class NextAppointment(CrfModelMixin, edc_models.BaseUuidModel):

    hiv_clinic_appt_date = models.DateField(
        verbose_name="HIV clinic: next scheduled routine appointment",
        null=True,
        blank=True,
        help_text="if applicable.",
    )

    ncd_clinic_appt_date = models.DateField(
        verbose_name="NCD clinic: next scheduled routine appointment",
        null=True,
        blank=True,
        help_text="if applicable.",
    )

    dm_clinic_appt_date = models.DateField(
        verbose_name="Diabetes-only clinic: next scheduled routine appointment",
        null=True,
        blank=True,
        help_text="if applicable.",
    )

    htn_clinic_appt_date = models.DateField(
        verbose_name="Hypertension-only clinic: next scheduled routine appointment",
        null=True,
        blank=True,
        help_text="if applicable.",
    )

    integrated_clinic_appt_date = models.DateField(
        verbose_name="Integrated clinic: next scheduled routine appointment",
        null=True,
        blank=True,
        help_text="if applicable.",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Routine Appointment"
        verbose_name_plural = "Routine Appointments"
