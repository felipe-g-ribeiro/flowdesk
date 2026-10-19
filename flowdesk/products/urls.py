from django.urls import path

from .views import (
    product_list,
    product_create,
    product_update,
    product_delete,
    category_list,
    category_create,
    category_update,
    category_delete,
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
    
    path(
    "excluir/<int:pk>/",
    product_delete,
    name="product_delete"
    ),
    path(
    "categorias/",
    category_list,
    name="category_list"
    ),

    path(
    "categorias/nova/",
    category_create,
    name="category_create"
    ),

    path(
    "categorias/editar/<int:pk>/",
    category_update,
    name="category_update"
    ),

    path(
    "categorias/excluir/<int:pk>/",
    category_delete,
    name="category_delete"
    ),
]