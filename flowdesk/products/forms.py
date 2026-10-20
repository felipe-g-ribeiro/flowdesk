from django import forms
from .models import Product, Category

 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "style": "color: #ffffff;"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "style": "color: #ffffff;"}),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "style": "text-align: center;",
                    "style": "color: #ffffff;",

                    
                }
            ),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        labels = {
            "name": "Nome",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control category-input"}
            ),
        }