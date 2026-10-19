from django import forms

from .models import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ["total"]
        fields = "__all__"
        labels = {
            "customer": "Cliente",
            "product": "Produto",
            "quantity": "Quantidade",
            
        }
        widgets = {
            "customer": forms.Select(
                attrs={"class": "form-control customer-input", "style": "background-color: #fff; color: #212529;"}
            ),
            "product": forms.Select(
                attrs={"class": "form-control customer-input", "style": "background-color: #fff; color: #212529;"}
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control customer-input", "style": "background-color: #fff; color: #212529;"}
            ),
            "total": forms.NumberInput(
                attrs={"class": "form-control customer-input", "style": "background-color: #fff; color: #212529;"}
            ),
        }
