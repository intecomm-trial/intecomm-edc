from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class CrfReportMixin:
    weight_model = "intecomm_subject.followup"

    @property
    def unblinded(self):
        UnblindingRequest = django_apps.get_model("intecomm_prn.unblindingrequest")
        try:
            unblinded = UnblindingRequest.objects.get(
                subject_identifier=self.subject_identifier, approved=True
            )
        except ObjectDoesNotExist:
            unblinded = False
        return unblinded
