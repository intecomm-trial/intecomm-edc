from django.db import models
from django.db.models import PROTECT
from edc_model import models as edc_models

from intecomm_screening.models import HealthFacility

from ..choices import APPT_DATE_INFO_SOURCES
from ..constants import INTEGRATED
from ..model_mixins import CrfModelMixin


def get_visit_code(mnth: int):
    if mnth < 10:
        return f"10{mnth*10}"
    return f"1{mnth*10}"


def visit_code_choices():
    codes = ["1000"]
    for i in range(1, 13):
        codes.append(get_visit_code(i))
    return tuple([(code, code) for code in codes])


class NextAppointment(CrfModelMixin, edc_models.BaseUuidModel):
    health_facility = models.ForeignKey(
        HealthFacility,
        on_delete=PROTECT,
        limit_choices_to={"health_facility_type__name": INTEGRATED},
        null=True,
        blank=True,
    )

    appt_date = models.DateField(
        verbose_name="Next scheduled routine/facility appointment",
        null=True,
        blank=False,
        help_text="Should fall on an Integrated clinic day",
    )
    info_source = models.CharField(
        verbose_name="What is the source of this appointment date",
        max_length=15,
        choices=APPT_DATE_INFO_SOURCES,
        null=True,
        blank=False,
    )

    best_visit_code = models.CharField(
        verbose_name="Which study visit code is closest to this appointment date",
        max_length=15,
        choices=visit_code_choices(),
        null=True,
        blank=False,
        help_text=(
            "Click SAVE to let the EDC suggest. Once selected, interim appointments will "
            "be flagged as not required."
        ),
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Next Appointment"
        verbose_name_plural = "Next Appointments"
