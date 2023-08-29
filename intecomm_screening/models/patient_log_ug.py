from .patient_log import PatientLog


class PatientLogUg(PatientLog):
    class Meta:
        proxy = True
        verbose_name = "Patient Log (Uganda)"
        verbose_name_plural = "Patient Log (Uganda)"
