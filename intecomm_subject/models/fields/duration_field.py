from django.utils.translation import gettext as _
from edc_model.validators import hm_validator
from edc_model_fields.fields import CharField2


class DurationAsStringField(CharField2):
    """Duration field class for hours/minutes"""

    def __init__(self, *args, **kwargs):
        self.custom_null = kwargs.get("null")
        self.custom_blank = kwargs.get("blank")
        if self.custom_blank is None:
            kwargs.update(blank=True)
        if self.custom_null is None:
            kwargs.update(null=True)
        kwargs.update(max_length=15)
        kwargs.update(validators=[hm_validator])
        if kwargs.get("help_text") is None:
            kwargs.update(
                help_text=_(
                    "Please insert a numeric value followed by “h” for hours, "
                    "and a numeric value followed by “m” for minutes. "
                    "For example, 1h2m, 0h35m, and so on"
                )
            )
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.custom_null is None:
            del kwargs["null"]
        if self.custom_blank is None:
            del kwargs["blank"]
        del kwargs["max_length"]
        del kwargs["validators"]
        del kwargs["help_text"]
        return name, path, args, kwargs
