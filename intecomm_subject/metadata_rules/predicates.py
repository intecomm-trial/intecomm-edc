from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import NO
from edc_metadata.metadata_rules import PredicateCollection


class Predicates(PredicateCollection):
    app_label = "intecomm_subject"
    visit_model = "intecomm_subject.subjectvisit"

    @staticmethod
    def household_head_required(visit, **kwargs):
        """Note: this is a singleton"""
        model_cls = django_apps.get_model("intecomm_subject.healtheconomicshouseholdhead")
        try:
            model_cls.objects.get(subject_visit__subject_identifier=visit.subject_identifier)
        except ObjectDoesNotExist:
            return True
        return False

    @staticmethod
    def patient_required(visit, **kwargs):
        """Note: this is a singleton"""
        required = False
        patient_model_cls = django_apps.get_model("intecomm_subject.healtheconomicspatient")
        hoh_model_cls = django_apps.get_model("intecomm_subject.healtheconomicshouseholdhead")
        try:
            hoh_obj = hoh_model_cls.objects.get(
                subject_visit__subject_identifier=visit.subject_identifier
            )
        except ObjectDoesNotExist:
            pass
        else:
            if not patient_model_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier
            ).exists():
                required = hoh_obj.hoh == NO
        return required

    @staticmethod
    def assets_required(visit, **kwargs):
        model_cls = django_apps.get_model("intecomm_subject.healtheconomicsassets")
        try:
            model_cls.objects.get(subject_visit__subject_identifier=visit.subject_identifier)
        except ObjectDoesNotExist:
            return True
        return False

    @staticmethod
    def property_required(visit, **kwargs):
        model_cls = django_apps.get_model("intecomm_subject.healtheconomicsproperty")
        try:
            model_cls.objects.get(subject_visit__subject_identifier=visit.subject_identifier)
        except ObjectDoesNotExist:
            return True
        return False

    @staticmethod
    def income_required(visit, **kwargs):
        model_cls = django_apps.get_model("intecomm_subject.healtheconomicsincome")
        try:
            model_cls.objects.get(subject_visit__subject_identifier=visit.subject_identifier)
        except ObjectDoesNotExist:
            return True
        return False
