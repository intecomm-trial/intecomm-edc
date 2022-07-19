from edc_action_item.forms import ActionItemFormMixin
from edc_adverse_event.forms import validate_ae_initial_outcome_date
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_registration.modelform_mixins import ModelFormSubjectIdentifierMixin


class AeReviewFormValidator(FormValidator):
    def clean(self):
        pass


class AeReviewModelFormMixin(
    ModelFormSubjectIdentifierMixin,
    ActionItemFormMixin,
    FormValidatorMixin,
):
    form_validator_cls = AeReviewFormValidator

    def clean(self):
        cleaned_data = super().clean()
        validate_ae_initial_outcome_date(self)
        return cleaned_data

    class Meta(ActionItemFormMixin.Meta):
        pass
