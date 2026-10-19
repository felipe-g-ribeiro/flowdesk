from django.urls import path
from .views import product_list
from .views import product_create


urlpatterns = [
    path("", product_list, name="product_list"),
    path("novo/", product_create, name="product_create"),
]