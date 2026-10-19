from django.urls import path

from .views import customer_list, customer_create, customer_update, customer_delete


urlpatterns = [
    path(
        "",
        customer_list,
        name="customer_list"
    ),

    path(
        "novo/",
        customer_create,
        name="customer_create"
    ),

    path(
        "editar/<int:pk>/",
        customer_update,
        name="customer_update"
    ),

    path(
        "excluir/<int:pk>/",
        customer_delete,
        name="customer_delete"
    ),
]