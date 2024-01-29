from .subject_consent import SubjectConsent


class SubjectConsentTz(SubjectConsent):
    class Meta(SubjectConsent.Meta):
        proxy = True
        verbose_name = "Subject Consent (Tanzania)"
        verbose_name_plural = "Subject Consents (Tanzania)"
