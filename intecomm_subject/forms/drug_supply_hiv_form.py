from django import forms

from ..models import ArvRegimens, DrugSupplyHiv


class DrugSupplyHivForm(forms.ModelForm):
    list_model_cls = ArvRegimens
    relation_label = "drugsupplyhiv"

    def clean(self):
        cleaned_data = super().clean()
        if (
            self.cleaned_data.get("drug")
            and self.cleaned_data.get("drug").name
            not in self.cleaned_data.get("drug_refill").rx.name
        ):
            raise forms.ValidationError(
                f"Invalid. `{self.cleaned_data.get('drug').display_name}` "
                "not in current regimen "
                f"`{self.cleaned_data.get('drug_refill').rx.display_name}`"
            )
        return cleaned_data

    class Meta:
        model = DrugSupplyHiv
        fields = "__all__"
