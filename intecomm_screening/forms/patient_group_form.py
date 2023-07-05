from django import forms
from edc_form_validators import FormValidatorMixin
from intecomm_form_validators import PatientGroupFormValidator

from ..models import PatientGroup


class PatientGroupForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = PatientGroupFormValidator

    def clean_hiv_patients(self):
        hiv_patients = self.cleaned_data.get("hiv_patients")
        self.raise_if_already_in_group("hiv_patients", hiv_patients)
        return hiv_patients

    def clean_htn_patients(self):
        htn_patients = self.cleaned_data.get("htn_patients")
        self.raise_if_already_in_group("htn_patients", htn_patients)
        return htn_patients

    def clean_dm_patients(self):
        dm_patients = self.cleaned_data.get("dm_patients")
        self.raise_if_already_in_group("dm_patients", dm_patients)
        return dm_patients

    def clean_multi_patients(self):
        multi_patients = self.cleaned_data.get("multi_patients")
        self.raise_if_already_in_group("multi_patients", multi_patients)
        return multi_patients

    def raise_if_already_in_group(self, attr, data):
        qs = self._meta.model.objects.filter(**{f"{attr}__in": list(data)}).exclude(
            name=self.cleaned_data.get("name")
        )
        if qs.count() >= 1:
            patients = list(data)
            for patient_group in qs:
                for patient_log in patient_group.patients.all():
                    if patient_log in patients:
                        raise forms.ValidationError(
                            f"Patient in another group. Got `{patient_log}` in "
                            f"group `{patient_group.name}`."
                        )

    class Meta:
        model = PatientGroup
        fields = "__all__"
