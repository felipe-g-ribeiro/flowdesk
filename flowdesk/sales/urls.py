from django.urls import path

from .views import (
    sale_list,
    sale_create,
    sale_update,
    sale_delete,
)

urlpatterns = [
    path(
        "",
        sale_list,
        name="sale_list"
    ),

    path(
        "novo/",
        sale_create,
        name="sale_create"
    ),

    path(
        "editar/<int:pk>/",
        sale_update,
        name="sale_update"
    ),

    path(
        "excluir/<int:pk>/",
        sale_delete,
        name="sale_delete"
    ),
]
