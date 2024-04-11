from intecomm_consent.consents import cdef_ug_v1

from .subject_screening import SubjectScreening


class SubjectScreeningUg(SubjectScreening):
    consent_definitions = [cdef_ug_v1]

    class Meta:
        proxy = True
        verbose_name = "Subject Screening (Uganda)"
        verbose_name_plural = "Subject Screening (Uganda)"
