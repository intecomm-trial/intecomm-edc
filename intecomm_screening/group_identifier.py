from django.apps import apps as django_apps
from edc_identifier.research_identifier import ResearchIdentifier
from edc_utils import get_utcnow


class GroupIdentifier(ResearchIdentifier):
    template: str = "{site_id}{sequence}"
    label: str = "groupidentifier"
    padding: int = 3

    def pre_identifier(self) -> None:
        pass

    def post_identifier(self) -> None:
        """Creates a registered group instance for this
        group identifier.
        """
        model = django_apps.get_model("intecomm_screening.registeredgroup")
        model.objects.create(
            group_identifier=self.identifier,
            site=self.site,
            registration_datetime=get_utcnow(),
        )
