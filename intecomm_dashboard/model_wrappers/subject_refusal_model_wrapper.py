from edc_model_wrapper import ModelWrapper


class ConsentRefusalModelWrapper(ModelWrapper):
    model = "intecomm_screening.consentrefusal"
    next_url_attrs = ["screening_identifier"]
    next_url_name = "screening_listboard_url"

    @property
    def pk(self):
        return str(self.object.pk)

    @property
    def screening_identifier(self):
        return self.object.screening.screening_identifier
