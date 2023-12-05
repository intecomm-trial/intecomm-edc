from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.html import format_html
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.choices import PREG_YES_NO_NA, SELECTION_METHOD, YES_NO, YES_NO_NA
from edc_constants.constants import NO, NOT_APPLICABLE, PURPOSIVELY_SELECTED, TBD
from edc_model.models import BaseUuidModel, DurationYMDField, NameFieldsModelMixin
from edc_screening.model_mixins import EligibilityModelMixin, ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)
from edc_vitals.model_mixins import BloodPressureModelMixin
from intecomm_eligibility import ScreeningEligibility

from .patient_log import PatientLog
from .proxy_models import Site


class SubjectScreeningError(Exception):
    pass


class ScreeningIdentifier(BaseScreeningIdentifier):
    template = "S{random_string}"


class SubjectScreening(
    EligibilityModelMixin,
    BloodPressureModelMixin,
    ScreeningModelMixin,
    NameFieldsModelMixin,
    BaseUuidModel,
):
    identifier_cls = ScreeningIdentifier
    eligibility_cls = ScreeningEligibility

    # declare `site` explicitly as editable by user
    # (instead of using modelmixin)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True, related_name="+")

    screening_identifier = models.CharField(
        verbose_name="Screening ID",
        max_length=50,
        blank=True,
        unique=True,
    )

    patient_log_identifier = models.CharField(
        verbose_name="Patient log identifier",
        max_length=50,
        unique=True,
    )

    patient_log = models.OneToOneField(
        PatientLog, on_delete=models.PROTECT, null=True, blank=True
    )

    selection_method = models.CharField(
        verbose_name="How was the patient selected for screening?",
        max_length=25,
        choices=SELECTION_METHOD,
        default=PURPOSIVELY_SELECTED,
    )

    hospital_identifier = EncryptedCharField(unique=True, blank=False)

    lives_nearby = models.CharField(
        verbose_name=(
            "Does the patient live within the catchment population of the health facility"
        ),
        max_length=15,
        choices=YES_NO,
    )

    staying_nearby_6 = models.CharField(
        verbose_name=(
            "Is the patient planning to remain in this catchment area for at least 6 months"
        ),
        max_length=15,
        choices=YES_NO,
    )

    in_care_6m = models.CharField(
        verbose_name=(
            "Has the patient been in regular care at this health facility for 6 months or more"
        ),
        max_length=15,
        choices=YES_NO,
        help_text="for 6m or more at the health facility from which they are being recruited",
    )

    in_care_duration = DurationYMDField(
        verbose_name=(
            "If 'Yes', estimate how long the patient been in regular care at this "
            "health facility"
        ),
        null=True,
        blank=True,
    )

    hiv_dx = models.CharField(
        verbose_name="Has the patient previously been diagnosed with HIV",
        max_length=15,
        choices=YES_NO,
    )

    hiv_dx_6m = models.CharField(
        verbose_name="Was the initial diagnosis made more than 6 months ago",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    hiv_dx_ago = DurationYMDField(
        verbose_name="If 'Yes', estimate how long ago the initial diagnosis was made",
        null=True,
        blank=True,
    )

    art_unchanged_3m = models.CharField(
        verbose_name=format_html(
            "Has the patient been on the same anti-retroviral therapy for at least 3 months"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Meaning no modifications to the type of medication and dose for at least 3 months"
        ),
    )

    art_stable = models.CharField(
        verbose_name="Is the patient considered to be stable on treatment ",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "considered by the clinical team not to have any complications/co-infections "
            "or that these are well managed."
        ),
    )

    art_adherent = models.CharField(
        verbose_name=(
            "Is the patient considered to be adherent to treatment over the last 6 months"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="in regular attendance for care",
    )

    dm_dx = models.CharField(
        verbose_name="Has the patient previously been diagnosed with Diabetes",
        max_length=15,
        choices=YES_NO,
    )

    dm_dx_6m = models.CharField(
        verbose_name="Was the initial diagnosis made more than 6 months ago",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    dm_dx_ago = DurationYMDField(
        verbose_name="If 'Yes', estimate how long ago the initial diagnosis was made",
        null=True,
        blank=True,
    )

    dm_complications = models.CharField(
        verbose_name=(
            "Does the patient suffer from any complications of diabetes that are "
            "unmanaged or uncontrolled."
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    htn_dx = models.CharField(
        verbose_name="Has the patient previously been diagnosed with Hypertension",
        max_length=15,
        choices=YES_NO,
    )

    htn_dx_6m = models.CharField(
        verbose_name="Was the initial diagnosis made more than 6 months ago",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    htn_dx_ago = DurationYMDField(
        verbose_name="If 'Yes', estimate how long ago the initial diagnosis was made",
        null=True,
        blank=True,
    )

    htn_complications = models.CharField(
        verbose_name=(
            "Does the patient suffer from any complications of hypertension that are "
            "unmanaged or uncontrolled."
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    excluded_by_bp_history = models.CharField(
        verbose_name=(
            "Has the patient's blood pressure exceeded 180/110 mmHg on more than "
            "one occasion any time in the last 6 months."
        ),
        max_length=15,
        choices=YES_NO,
    )

    excluded_by_gluc_history = models.CharField(
        verbose_name=(
            "Has the patient's blood glucose exceeded 13 mmol/L any time in the last 6 months."
        ),
        max_length=15,
        choices=YES_NO,
    )

    requires_acute_care = models.CharField(
        verbose_name=(
            "Does the patient have any clinical condition that requires health "
            "facility management"
        ),
        max_length=15,
        choices=YES_NO,
    )

    pregnant = models.CharField(
        verbose_name="Is the patient pregnant?", max_length=15, choices=PREG_YES_NO_NA
    )

    def __str__(self):
        return (
            f"{self._meta.verbose_name} {self.screening_identifier} "
            f"{self.age_in_years}{self.gender}"
        )

    def save(self, *args, **kwargs):
        try:
            self.patient_log = PatientLog.objects.get(
                patient_log_identifier=self.patient_log_identifier
            )
        except ObjectDoesNotExist:
            raise SubjectScreeningError(
                f"Invalid patient log identifier. Got `{self.patient_log_identifier}`. "
                "Perhaps catch this in the form."
            )
        if self.patient_log:
            if self.patient_log.willing_to_screen == NO:
                raise SubjectScreeningError(
                    f"Patient '{self.patient_log.patient_log_identifier}' is unwilling to "
                    f"screen. Got reason '{self.patient_log.screening_refusal_reason}' "
                    "Perhaps catch this in the form."
                )
            elif self.patient_log.willing_to_screen == TBD:
                raise SubjectScreeningError(
                    f"Patient '{self.patient_log.patient_log_identifier}' has not indicated "
                    f"willingness to screen. Got `{TBD}`. Perhaps catch this in the form. "
                )
            if self.patient_log.hospital_identifier != self.hospital_identifier:
                raise SubjectScreeningError(
                    "Health facility identifier does not match patient log. "
                    f"Got {self.patient_log.hospital_identifier}!={self.hospital_identifier}. "
                    "Perhaps catch this in the form."
                )
            if self.patient_log.initials != self.initials:
                raise SubjectScreeningError(
                    "Initials do not match patient log. "
                    f"Got {self.patient_log.initials}!={self.initials}. "
                    "Perhaps catch this in the form."
                )
        super().save(*args, **kwargs)

    @property
    def patient_group(self):
        return self.patient_log.patientgroup_set.all().first()

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
        constraints = [
            UniqueConstraint(
                fields=["legal_name", "initials"], name="%(app_label)s_%(class)s_legal_n_uniq"
            )
        ]
        indexes = ScreeningModelMixin.Meta.indexes + BaseUuidModel.Meta.indexes
