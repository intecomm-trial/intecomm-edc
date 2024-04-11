from django.core.exceptions import ObjectDoesNotExist
from edc_identifier.identifier import Identifier
from edc_identifier.simple_identifier import SimpleUniqueIdentifier


class PatientLogIdentifier(SimpleUniqueIdentifier):
    name = "patient_log_identifier"
    template = "P{random_string}"
    random_string_length: int = 7


class FilingIdentifier(Identifier):
    name = "filing_identifier"
    identifier_pattern = r"^[0-9]{3}-\d+$"
    separator = "-"
    prefix = "F"

    def __init__(self, site_id: int = None, **kwargs):
        self.site_id = str(site_id)
        super().__init__(**kwargs)

    def next_identifier(self):
        """Sets the next identifier and updates the identifier model."""
        segment = self.remove_separator(self.identifier)[1:]
        if not segment or segment == "0":
            segment = int(f"{self.site_id}{'10000'}")
        segment = str(int(segment) + 1)
        self.identifier = f"{self.prefix}{segment[0:3]}{self.separator}{segment[3:]}"
        self.update_identifier_model()

    @property
    def last_identifier(self):
        """Returns the last identifier in the identifier model."""
        last_identifier = None
        opts = dict(
            identifier_type=self.name,
            identifier__istartswith=f"{self.prefix}{self.site_id}",
        )
        try:
            instance = (
                self.identifier_model_cls.objects.filter(**opts).order_by("identifier").last()
            )
        except AttributeError:
            pass
        else:
            if instance:
                last_identifier = instance.identifier
        return last_identifier

    def validate_identifier_pattern(self, *args, **kwargs):
        return True

    def update_identifier_model(self) -> bool:
        """Attempts to update identifier_model and returns True (or instance)
        if successful else False if identifier already exists.
        """
        try:
            self.identifier_model_cls.objects.get(identifier=self.identifier)
        except ObjectDoesNotExist:
            return self.identifier_model_cls.objects.create(
                identifier=self.identifier,
                identifier_type=self.name,
                identifier_prefix=self.identifier_prefix,
                device_id=self.device_id,
                site_id=self.site_id,
            )
        return False
