from edc_consent.managers import ConsentObjectsByCdefManager, CurrentSiteByCdefManager

from .subject_consent import SubjectConsent


class SubjectConsentTz(SubjectConsent):

    objects = ConsentObjectsByCdefManager()

    on_site = CurrentSiteByCdefManager()

    class Meta(SubjectConsent.Meta):
        proxy = True
        verbose_name = "Subject Consent (Tanzania)"
        verbose_name_plural = "Subject Consents (Tanzania)"
