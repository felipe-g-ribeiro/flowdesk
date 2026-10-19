from django.urls import path

from .views import (
    product_list,
    product_create,
    product_update,
)

urlpatterns = [
    path("", product_list, name="product_list"),

    path(
        "novo/",
        product_create,
        name="product_create"
    ),

    path(
        "editar/<int:pk>/",
        product_update,
        name="product_update"
    ),
]