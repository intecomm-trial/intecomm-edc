from .subject_screening import SubjectScreening


class SubjectScreeningUg(SubjectScreening):
    class Meta:
        proxy = True
        verbose_name = "Subject Screening (Uganda)"
        verbose_name_plural = "Subject Screening (Uganda)"
