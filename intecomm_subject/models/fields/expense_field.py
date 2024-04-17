from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _
from edc_model_fields.fields import IntegerField2


class ExpenseField(IntegerField2):
    def __init__(self, *args, **kwargs):
        self.custom_null = kwargs.get("null")
        self.custom_blank = kwargs.get("blank")
        if self.custom_null is None:
            kwargs.update(null=True)
        if self.custom_blank is None:
            kwargs.update(blank=True)
        kwargs.update(validators=[MinValueValidator(0), MaxValueValidator(9999999)])
        if kwargs.get("blank"):
            default_help_text = _(
                "In local currency. If nothing spent enter `0` or leave blank "
                "if a response is not required."
            )
        else:
            default_help_text = _("In local currency. If nothing spent enter `0`.")
        self.custom_help_text = kwargs.get("help_text")
        kwargs.update(help_text=self.custom_help_text or default_help_text)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["validators"]
        if self.custom_help_text is None:
            del kwargs["help_text"]
        if self.custom_null is None:
            del kwargs["null"]
        if self.custom_blank is None:
            del kwargs["blank"]
        return name, path, args, kwargs
