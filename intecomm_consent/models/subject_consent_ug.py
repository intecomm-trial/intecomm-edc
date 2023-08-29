from edc_consent.constants import DEFAULT_CONSENT_GROUP

from .subject_consent import SubjectConsent


class SubjectConsentUg(SubjectConsent):
    class Meta(SubjectConsent.Meta):
        proxy = True
        verbose_name = "Subject Consent (Uganda)"
        verbose_name_plural = "Subject Consents (Uganda)"
        consent_group = DEFAULT_CONSENT_GROUP
