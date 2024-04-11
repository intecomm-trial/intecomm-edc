from edc_consent.managers import ConsentObjectsByCdefManager, CurrentSiteByCdefManager

from .subject_consent import SubjectConsent


class SubjectConsentUg(SubjectConsent):

    objects = ConsentObjectsByCdefManager()

    on_site = CurrentSiteByCdefManager()

    class Meta(SubjectConsent.Meta):
        proxy = True
        verbose_name = "Subject Consent (Uganda)"
        verbose_name_plural = "Subject Consents (Uganda)"
