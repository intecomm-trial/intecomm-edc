from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_adverse_event.form_validator_mixins import (
    RequiresDeathReportFormValidatorMixin,
)
from edc_consent.constants import CONSENT_WITHDRAWAL
from edc_constants.constants import DEAD, TOXICITY
from edc_form_validators import INVALID_ERROR, FormValidator
from edc_ltfu.constants import LTFU
from edc_ltfu.modelform_mixins import RequiresLtfuFormValidatorMixin
from edc_offstudy.constants import COMPLETED_FOLLOWUP
from edc_offstudy.utils import OffstudyError
from edc_prn.modelform_mixins import PrnFormValidatorMixin
from edc_transfer.constants import TRANSFERRED
from edc_utils import formatted_date
from edc_visit_schedule.constants import MONTH36
from edc_visit_schedule.utils import off_all_schedules_or_raise

from ..constants import CLINICAL_WITHDRAWAL, INVESTIGATOR_DECISION


class EndOfStudyFormValidator(
    RequiresDeathReportFormValidatorMixin,
    RequiresLtfuFormValidatorMixin,
    PrnFormValidatorMixin,
    FormValidator,
):
    death_report_model = "meta_ae.deathreport"
    ltfu_model = None

    def clean(self):

        self.confirm_off_all_schedules()
        self.validate_offstudy_datetime_against_last_seen_date()

        self.validate_completed_36m()

        self.required_if(DEAD, field="offstudy_reason", field_required="death_date")
        self.validate_death_report_if_deceased()

        self.required_if(TRANSFERRED, field="offstudy_reason", field_required="transfer_date")
        self.validate_transfer()

        self.required_if(LTFU, field="offstudy_reason", field_required="ltfu_date")
        self.validate_ltfu()

        self.applicable_if(
            TOXICITY, field="offstudy_reason", field_applicable="toxicity_withdrawal_reason"
        )
        self.validate_other_specify(
            field="toxicity_withdrawal_reason",
            other_specify_field="toxicity_withdrawal_reason_other",
        )

        self.applicable_if(
            CLINICAL_WITHDRAWAL,
            field="offstudy_reason",
            field_applicable="clinical_withdrawal_reason",
        )

        self.validate_other_specify(
            other_stored_value=INVESTIGATOR_DECISION,
            field="clinical_withdrawal_reason",
            other_specify_field="clinical_withdrawal_investigator_decision",
        )

        self.validate_other_specify(
            field="clinical_withdrawal_reason",
            other_specify_field="clinical_withdrawal_reason_other",
        )

        self.required_if(
            CONSENT_WITHDRAWAL,
            field="offstudy_reason",
            field_required="consent_withdrawal_reason",
        )

    def validate_completed_36m(self):
        if (
            self.cleaned_data.get("offstudy_reason")
            and self.cleaned_data.get("offstudy_reason").name == COMPLETED_FOLLOWUP
        ):
            subject_visit_model_cls = django_apps.get_model("intecomm_subject.subjectvisit")
            try:
                subject_visit_model_cls.objects.get(
                    subject_identifier=self.subject_identifier,
                    visit_code=MONTH36,
                    visit_code_sequence=0,
                )
            except ObjectDoesNotExist:
                self.raise_validation_error(
                    {"offstudy_reason": "Invalid. 36 month visit has not been submitted."},
                    INVALID_ERROR,
                )

    def confirm_off_all_schedules(self):
        try:
            off_all_schedules_or_raise(
                subject_identifier=self.cleaned_data.get("subject_identifier"),
            )
        except OffstudyError as e:
            self.raise_validation_error(str(e), INVALID_ERROR)

    def validate_offstudy_datetime_against_last_seen_date(self):
        if self.cleaned_data.get("offstudy_datetime") and self.cleaned_data.get(
            "last_seen_date"
        ):
            if (
                self.cleaned_data.get("last_seen_date")
                > self.cleaned_data.get("offstudy_datetime").date()
            ):
                raise forms.ValidationError(
                    {"last_seen_date": "Invalid. May not be after termination date"}
                )

    def validate_transfer(self):
        if (
            self.cleaned_data.get("offstudy_reason")
            and self.cleaned_data.get("offstudy_reason").name == TRANSFERRED
        ):
            transfer_model_cls = django_apps.get_model("intecomm_prn.subjecttransfer")
            try:
                obj = transfer_model_cls.objects.get(
                    subject_visit__subject_identifier=self.subject_identifier,
                )
            except ObjectDoesNotExist:
                self.raise_validation_error(
                    {
                        "offstudy_reason": (
                            f"Invalid. {transfer_model_cls._meta.verbose_name} "
                            "has not been submitted."
                        )
                    },
                    INVALID_ERROR,
                )
            else:
                if obj.transfer_date.date() != self.cleaned_data.get("transfer_date"):
                    dt = formatted_date(obj.transfer_date)
                    self.raise_validation_error(
                        {
                            "transfer_date": (
                                "Invalid. Does not match date on "
                                f"{transfer_model_cls._meta.verbose_name}. Expected {dt}."
                            )
                        },
                        INVALID_ERROR,
                    )
