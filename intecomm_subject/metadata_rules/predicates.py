from django.apps import apps as django_apps
from edc_metadata.metadata_rules import PredicateCollection
from edc_visit_schedule.utils import is_baseline


class Predicates(PredicateCollection):

    app_label = "intecomm_subject"
    visit_model = "intecomm_subject.subjectvisit"

    @staticmethod
    def family_history_required(visit, **kwargs):
        """Returns True if this is not the baseline visit
        and the CRF has NOT been previously completed.
        """
        required = False
        if not is_baseline(visit):
            model_cls = django_apps.get_model("intecomm_subject.familyhistory")
            if not model_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier,
            ).exists():
                required = True
        return required
