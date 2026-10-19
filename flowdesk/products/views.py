from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import CategoryForm, ProductForm

from .models import Product
from .forms import ProductForm

from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):

   
    search = request.GET.get("search")

    products = Product.objects.all()
    
    if search:
        products = products.filter(
            name__icontains=search
        )
        
    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )

@login_required
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

@login_required
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

@login_required
def product_delete(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk
    )

    product.delete()

    return redirect("product_list")

@login_required
def category_list(request):
    categories = Category.objects.all()

    return render(
        request,
        "products/category_list.html",
        {"categories": categories}
    )

@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("category_list")

    return render(
        request,
        "products/category_form.html",
        {"form": form}
    )

@login_required
def category_update(request, pk):
    category = get_object_or_404(
        Category,
        pk=pk
    )

    form = CategoryForm(
        request.POST or None,
        instance=category
    )

    if form.is_valid():
        form.save()
        return redirect("category_list")

    return render(
        request,
        "products/category_form.html",
        {"form": form}
    )

@login_required
def category_delete(request, pk):
    category = get_object_or_404(
        Category,
        pk=pk
    )

    category.delete()

    return redirect("category_list")
