from django.core.exceptions import ObjectDoesNotExist
from edc_subject_model_wrappers import AppointmentModelWrapper as Base

from intecomm_subject.models import SubjectVisitMissed


class AppointmentModelWrapper(Base):
    @property
    def subject_visit_missed(self) -> SubjectVisitMissed:
        obj = None
        if self.object.related_visit:
            opts = dict(subject_visit=self.object.related_visit)
            try:
                obj = SubjectVisitMissed.objects.get(**opts)
            except ObjectDoesNotExist:
                pass
        return obj
