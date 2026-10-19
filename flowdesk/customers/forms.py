from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "phone": "Telefone",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control customer-input", "style": "background-color: #fff; color: #212529;"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control customer-input", "style": "background-color: #fff; color: #212529;"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control customer-input", "style": "background-color: #fff; color: #212529;"}
            ),
        }