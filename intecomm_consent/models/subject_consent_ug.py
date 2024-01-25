from .subject_consent import SubjectConsent


class SubjectConsentUg(SubjectConsent):
    class Meta(SubjectConsent.Meta):
        proxy = True
        verbose_name = "Subject Consent (Uganda)"
        verbose_name_plural = "Subject Consents (Uganda)"
