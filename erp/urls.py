from django.urls import path

from . import views

app_name = "erp"

urlpatterns = [
    path("", views.index_redirect, name="index"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("categorias/", views.CategoriaListView.as_view(), name="categoria_list"),
    path("categorias/nova/", views.CategoriaCreateView.as_view(), name="categoria_create"),
    path("categorias/<int:pk>/editar/", views.CategoriaUpdateView.as_view(), name="categoria_update"),
    path("categorias/<int:pk>/remover/", views.CategoriaDeleteView.as_view(), name="categoria_delete"),
    path("produtos/", views.ProdutoListView.as_view(), name="produto_list"),
    path("produtos/novo/", views.ProdutoCreateView.as_view(), name="produto_create"),
    path("produtos/<int:pk>/editar/", views.ProdutoUpdateView.as_view(), name="produto_update"),
    path("produtos/<int:pk>/remover/", views.ProdutoDeleteView.as_view(), name="produto_delete"),
    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("clientes/novo/", views.ClienteCreateView.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/editar/", views.ClienteUpdateView.as_view(), name="cliente_update"),
    path("clientes/<int:pk>/remover/", views.ClienteDeleteView.as_view(), name="cliente_delete"),
    path("vendas/", views.VendaListView.as_view(), name="venda_list"),
    path("vendas/nova/", views.VendaCreateView.as_view(), name="venda_create"),
    path("vendas/<int:pk>/", views.VendaDetailView.as_view(), name="venda_detail"),
    path("vendas/<int:pk>/editar/", views.VendaUpdateView.as_view(), name="venda_update"),
    path("vendas/<int:pk>/remover/", views.VendaDeleteView.as_view(), name="venda_delete"),
    path("vendas/<int:pk>/itens/novo/", views.VendaItemCreateView.as_view(), name="venda_item_create"),
]
