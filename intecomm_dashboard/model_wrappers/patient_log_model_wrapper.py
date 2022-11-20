from edc_model_wrapper import ModelWrapper


class PatientLogModelWrapper(ModelWrapper):

    model = "intecomm_screening.patientlog"
    next_url_attrs = ["patient_log_identifier"]
    next_url_name = "patient_log_listboard_url"

    @property
    def human_screening_identifier(self):
        human = None
        if self.patient_log_identifier:
            human = f"{self.patient_log_identifier[0:4]}-{self.patient_log_identifier[4:]}"
        return human or self.patient_log_identifier
