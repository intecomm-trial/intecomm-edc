from intecomm_group.models import PatientGroup as BasePatientGroup


class PatientGroupRando(BasePatientGroup):
    def __str__(self):
        status = " (R)" if self.randomized else ""
        return f"{self.name.upper()}{status}"

    class Meta:
        proxy = True
        verbose_name = "Patient group randomization"
        verbose_name_plural = "Patient group randomization"
