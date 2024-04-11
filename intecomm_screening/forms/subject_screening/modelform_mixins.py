from __future__ import annotations

from typing import Type

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from edc_constants.constants import DM, HIV, HTN, NO, TBD, YES
from edc_dashboard.url_names import url_names
from edc_form_validators import INVALID_ERROR
from intecomm_form_validators import SubjectScreeningFormValidator
from intecomm_rando.constants import UGANDA

from ...models import PatientLog, PatientLogUg


class SubjectScreeningModelFormMixin:
    form_validator_cls = SubjectScreeningFormValidator

    def __init__(self, *args, **kwargs):
        self._patient_log = None
        super().__init__(*args, **kwargs)

    def clean(self) -> dict:
        self.validate_willing_to_screen_on_patient_log()
        self.validate_gender_against_patient_log()
        self.validate_stable_in_care_on_patient_log()
        self.validate_health_talks_on_patient_log()
        self.validate_initials_against_patient_log()
        self.validate_age_in_years_against_patient_log()
        self.validate_hospital_identifier_against_patient_log()
        self.validate_condition(HIV, "hiv_dx")
        self.validate_condition(DM, "dm_dx")
        self.validate_condition(HTN, "htn_dx")

        return super().clean()

    @property
    def patient_log_model_cls(self) -> Type[PatientLog | PatientLogUg]:
        pass

    @property
    def patient_log(self) -> PatientLog | PatientLogUg:
        if not self._patient_log:
            try:
                self._patient_log = self.patient_log_model_cls.objects.get(
                    patient_log_identifier=self.cleaned_data.get("patient_log_identifier")
                )
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    {"patient_log_identifier": "Invalid. Patient log identifier not found."}
                )
            if self._patient_log:
                if self._patient_log.site.siteprofile.country == UGANDA:
                    self._patient_log = PatientLogUg.objects.get(
                        patient_log_identifier=self.cleaned_data.get("patient_log_identifier")
                    )
        return self._patient_log

    @property
    def patient_log_link(self):
        return (
            f'<a href="{self.patient_log.get_changelist_url()}?'
            f'q={str(self.patient_log.id)}">{self.patient_log._meta.verbose_name}</a>'
        )

    def validate_willing_to_screen_on_patient_log(self):
        if self.patient_log.willing_to_screen:
            if self.patient_log.willing_to_screen == NO:
                errmsg = format_html(
                    f"Invalid. Patient is unwilling to screen. See {self.patient_log_link}."
                )
                raise forms.ValidationError(errmsg, code=INVALID_ERROR)
            elif self.patient_log.willing_to_screen == TBD:
                errmsg = format_html(
                    "Invalid. Patient has not yet agreed to screen. "
                    f"See {self.patient_log_link}."
                )
                raise forms.ValidationError(errmsg, code=INVALID_ERROR)

    def validate_stable_in_care_on_patient_log(self) -> None:
        if self.patient_log.stable != YES:
            errmsg = format_html(
                "Invalid. Patient is NOT known to be stable and in-care. "
                f"See {self.patient_log_link}."
            )
            raise forms.ValidationError(errmsg, code=INVALID_ERROR)

    def validate_health_talks_on_patient_log(self) -> None:
        if self.patient_log.first_health_talk not in [YES, NO]:
            errmsg = format_html(
                "Invalid. Has patient attended the first health talk? "
                f"See {self.patient_log_link}."
            )
            raise forms.ValidationError(errmsg, code=INVALID_ERROR)
        elif self.patient_log.second_health_talk not in [YES, NO]:
            errmsg = format_html(
                "Invalid. Has patient attended the second health talk? "
                f"See {self.patient_log_link}."
            )
            raise forms.ValidationError(errmsg, code=INVALID_ERROR)

    def validate_gender_against_patient_log(self) -> None:
        if self.cleaned_data.get("gender") != self.patient_log.gender:
            raise forms.ValidationError(
                {
                    "gender": format_html(
                        f"Invalid. Expected {self.patient_log.get_gender_display()}. "
                        f"See {self.patient_log_link}."
                    )
                },
                code=INVALID_ERROR,
            )

    def validate_age_in_years_against_patient_log(self):
        if self.cleaned_data.get("age_in_years") != self.patient_log.age_in_years:
            raise forms.ValidationError(
                {
                    "age_in_years": format_html(
                        f"Invalid. Expected {self.patient_log.age_in_years}. "
                        f"See {self.patient_log_link}."
                    )
                },
                code=INVALID_ERROR,
            )

    def validate_initials_against_patient_log(self):
        if self.cleaned_data.get("initials") != self.patient_log.initials:
            raise forms.ValidationError(
                {
                    "initials": format_html(
                        f"Invalid. Expected {self.patient_log.initials}. "
                        f"See {self.patient_log_link}."
                    )
                },
                code=INVALID_ERROR,
            )

    def validate_hospital_identifier_against_patient_log(self):
        if (
            self.cleaned_data.get("hospital_identifier")
            != self.patient_log.hospital_identifier
        ):
            raise forms.ValidationError(
                {
                    "hospital_identifier": format_html(
                        f"Invalid. Expected {self.patient_log.hospital_identifier}. "
                        f"See {self.patient_log_link}."
                    )
                },
                code=INVALID_ERROR,
            )

    def validate_condition(self, name, field):
        if self.patient_log.conditions.count() == 0:
            raise forms.ValidationError(
                format_html(
                    "No conditions (HIV/DM/HTN) have been indicated for this patient. "
                    f"See {self.patient_log_link}."
                ),
                code=INVALID_ERROR,
            )
        else:
            if (
                not self.patient_log.conditions.filter(name=name)
                and self.cleaned_data.get(field) == YES
            ):
                raise forms.ValidationError(
                    {
                        field: format_html(
                            "Invalid. Condition not indicated "
                            f"on the Patient Log. Got {name.upper()}. "
                            f"See {self.patient_log_link}."
                        ),
                    },
                    code=INVALID_ERROR,
                )
            elif (
                self.patient_log.conditions.filter(name=name)
                and self.cleaned_data.get(field) == NO
            ):
                raise forms.ValidationError(
                    {
                        field: format_html(
                            f"Invalid. {name.upper()} was indicated "
                            "as a condition on the Patient Log. "
                            f"See {self.patient_log_link}."
                        ),
                    },
                    code=INVALID_ERROR,
                )

    def already_consented_validation_url(self, cleaned_data: dict | None = None) -> str:
        if self.instance.patient_log.group_identifier:
            url_name = url_names.get("subject_dashboard_url")
            url = reverse(
                url_name,
                kwargs={"subject_identifier": self.instance.subject_identifier},
            )
        else:
            if self.instance.site.siteprofile.country == UGANDA:
                url = reverse(
                    "intecomm_screening_admin:intecomm_screening_patientlogug_changelist"
                )
            else:
                url = reverse(
                    "intecomm_screening_admin:intecomm_screening_patientlog_changelist"
                )
            url = f"{url}?q={self.instance.subject_identifier}"
        return url
