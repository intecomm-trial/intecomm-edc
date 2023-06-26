from django import forms
from django.urls.base import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_dashboard.url_names import url_names
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import ConsentRefusalFormValidator

from intecomm_consent.utils import (
    AlreadyConsentedError,
    MultipleConsentsDetectedError,
    raise_if_already_consented,
)

from ..models import ConsentRefusal, SubjectScreening
from ..utils import get_add_or_change_consent_url


class RefusalFormMixin:
    def clean(self):
        cleaned_data = super().clean()
        subject_screening = cleaned_data.get("subject_screening")
        if subject_screening:
            self.validate_is_eligible(subject_screening=subject_screening)

            self.validate_not_already_consented(subject_screening=subject_screening)

        return cleaned_data

    @staticmethod
    def validate_is_eligible(subject_screening: SubjectScreening) -> None:
        if not subject_screening.eligible:
            url_name = url_names.get("screening_listboard_url")
            url = reverse(
                url_name,
                kwargs={"screening_identifier": subject_screening.screening_identifier},
            )
            msg = format_html(
                'Not allowed. Subject is not eligible. See subject <A href="{}">{}</A>',
                mark_safe(url),  # nosec B308 B703
                subject_screening.screening_identifier,
            )
            raise forms.ValidationError(msg)

    @staticmethod
    def validate_not_already_consented(subject_screening: SubjectScreening) -> None:
        try:
            raise_if_already_consented(
                screening_identifier=subject_screening.screening_identifier
            )
        except AlreadyConsentedError:
            _, consent_url, subject_identifier = get_add_or_change_consent_url(
                obj=subject_screening
            )
            msg = format_html(
                'Not allowed. Subject has already consented. See subject <A href="{}">{}</A>',
                mark_safe(consent_url),  # nosec B308 B703
                subject_identifier,
            )
            raise forms.ValidationError(msg)
        except MultipleConsentsDetectedError:
            raise forms.ValidationError(
                "Not allowed. Multiple subject consents detected "
                f"for subject '{subject_screening.screening_identifier}'. "
                "Inform data manager before continuing."
            )


class ConsentRefusalForm(RefusalFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = ConsentRefusalFormValidator

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = ConsentRefusal
        fields = "__all__"
        help_texts = {"subject_screening": "(read-only)"}
        widgets = {"subject_screening": forms.TextInput(attrs={"readonly": "readonly"})}
