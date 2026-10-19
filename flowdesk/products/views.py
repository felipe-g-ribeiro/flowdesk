from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import Product
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )


def product_create(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("product_list")

    return render(
        request,
        "products/product_form.html",
        {"form": form}
    )


def product_update(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk
    )

    form = ProductForm(
        request.POST or None,
        instance=product
    )

    if form.is_valid():
        form.save()
        return redirect("product_list")

    return render(
        request,
        "products/product_form.html",
        {"form": form}
    )