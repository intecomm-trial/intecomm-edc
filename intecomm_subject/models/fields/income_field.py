from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _
from edc_model_fields.fields import IntegerField2


class IncomeField(IntegerField2):
    def __init__(self, *args, **kwargs):
        kwargs.update(validators=[MinValueValidator(0), MaxValueValidator(9999999)])
        default_help_text = _(
            "In local currency. Ask for cash value or equivalent cash value for in-kind"
        )

        self.custom_help_text = kwargs.get("help_text")
        kwargs.update(help_text=self.custom_help_text or default_help_text)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["validators"]
        if not self.custom_help_text:
            del kwargs["help_text"]
        return name, path, args, kwargs
