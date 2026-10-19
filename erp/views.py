from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import CategoriaForm, ClienteForm, ItemVendaForm, ProdutoForm, VendaForm
from .models import Categoria, Cliente, ItemVenda, Produto, Venda


class HtmxTemplateMixin:
    partial_template_name = None

    def get_template_names(self):
        if self.request.headers.get("HX-Request") and self.partial_template_name:
            return [self.partial_template_name]
        return [self.template_name]


class HtmxRedirectMixin:
    def _get_htmx_redirect_response(self):
        return HttpResponse(status=204, headers={"HX-Redirect": str(self.get_success_url())})

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("HX-Request"):
            return self._get_htmx_redirect_response()
        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.headers.get("HX-Request"):
            return self._get_htmx_redirect_response()
        return response


class DashboardView(TemplateView):
    template_name = "erp/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["indicadores"] = {
            "produtos": Produto.objects.count(),
            "categorias": Categoria.objects.count(),
            "clientes": Cliente.objects.count(),
            "vendas": Venda.objects.count(),
        }
        context["top_produtos"] = Produto.objects.annotate(total_vendas=Count("itens_venda")).order_by("-total_vendas", "nome")[:5]
        return context


class CategoriaListView(ListView):
    model = Categoria
    template_name = "erp/categoria_list.html"


class CategoriaCreateView(HtmxRedirectMixin, HtmxTemplateMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "erp/form.html"
    partial_template_name = "erp/partials/form.html"
    success_url = reverse_lazy("erp:categoria_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nova categoria"
        return context


class CategoriaUpdateView(CategoriaCreateView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar categoria"
        return context


class CategoriaDeleteView(HtmxRedirectMixin, HtmxTemplateMixin, DeleteView):
    model = Categoria
    template_name = "erp/confirm_delete.html"
    partial_template_name = "erp/partials/confirm_delete.html"
    success_url = reverse_lazy("erp:categoria_list")


class ProdutoListView(ListView):
    model = Produto
    template_name = "erp/produto_list.html"


class ProdutoCreateView(HtmxRedirectMixin, HtmxTemplateMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "erp/form.html"
    partial_template_name = "erp/partials/form.html"
    success_url = reverse_lazy("erp:produto_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Novo produto"
        return context


class ProdutoUpdateView(ProdutoCreateView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar produto"
        return context


class ProdutoDeleteView(HtmxRedirectMixin, HtmxTemplateMixin, DeleteView):
    model = Produto
    template_name = "erp/confirm_delete.html"
    partial_template_name = "erp/partials/confirm_delete.html"
    success_url = reverse_lazy("erp:produto_list")


class ClienteListView(ListView):
    model = Cliente
    template_name = "erp/cliente_list.html"


class ClienteCreateView(HtmxRedirectMixin, HtmxTemplateMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "erp/form.html"
    partial_template_name = "erp/partials/form.html"
    success_url = reverse_lazy("erp:cliente_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Novo cliente"
        return context


class ClienteUpdateView(ClienteCreateView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar cliente"
        return context


class ClienteDeleteView(HtmxRedirectMixin, HtmxTemplateMixin, DeleteView):
    model = Cliente
    template_name = "erp/confirm_delete.html"
    partial_template_name = "erp/partials/confirm_delete.html"
    success_url = reverse_lazy("erp:cliente_list")


class VendaListView(ListView):
    model = Venda
    template_name = "erp/venda_list.html"


class VendaCreateView(HtmxRedirectMixin, HtmxTemplateMixin, CreateView):
    model = Venda
    form_class = VendaForm
    template_name = "erp/form.html"
    partial_template_name = "erp/partials/form.html"
    success_url = reverse_lazy("erp:venda_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nova venda"
        return context


class VendaUpdateView(VendaCreateView, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar venda"
        return context


class VendaDeleteView(HtmxRedirectMixin, HtmxTemplateMixin, DeleteView):
    model = Venda
    template_name = "erp/confirm_delete.html"
    partial_template_name = "erp/partials/confirm_delete.html"
    success_url = reverse_lazy("erp:venda_list")


class VendaDetailView(DetailView):
    model = Venda
    template_name = "erp/venda_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_form"] = kwargs.get("item_form") or ItemVendaForm()
        return context


class VendaItemCreateView(DetailView):
    model = Venda

    def post(self, request, *args, **kwargs):
        venda = self.get_object()
        form = ItemVendaForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.venda = venda
            item.save()
            form = ItemVendaForm()

        context = {"object": venda, "item_form": form}
        if request.headers.get("HX-Request"):
            return render(request, "erp/partials/sale_items_section.html", context)

        if form.errors:
            return render(request, "erp/venda_detail.html", context)
        return HttpResponseRedirect(reverse_lazy("erp:venda_detail", kwargs={"pk": venda.pk}))


def index_redirect(request):
    return HttpResponseRedirect(reverse_lazy("erp:dashboard"))
