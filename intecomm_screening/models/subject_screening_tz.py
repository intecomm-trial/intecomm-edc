from intecomm_consent.consents import cdef_tz_v1

from .subject_screening import SubjectScreening


class SubjectScreeningTz(SubjectScreening):
    consent_definitions = [cdef_tz_v1]

    class Meta:
        proxy = True
        verbose_name = "Subject Screening (Tanzania)"
        verbose_name_plural = "Subject Screening (Tanzania)"
