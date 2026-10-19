from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import Sale
from .forms import SaleForm

from django.contrib.auth.decorators import login_required

@login_required
def sale_list(request):
    sales = Sale.objects.all()

    return render(
        request,
        "sales/sale_list.html",
        {"sales": sales}
    )

@login_required
def sale_create(request):
    form = SaleForm(request.POST or None)

    if form.is_valid():
        sale = form.save(commit=False)

        sale.total = (
            sale.product.price * sale.quantity
        )

        product = sale.product

        if sale.quantity > product.stock:
            form.add_error(
                "quantity",
                "Estoque insuficiente."
            )

            return render(
                request,
                "sales/sale_form.html",
                {"form": form}
            )

        sale.save()

        product.stock -= sale.quantity
        product.save()

        return redirect("sale_list")

    return render(
        request,
        "sales/sale_form.html",
        {"form": form}
    )

    

       


@login_required
def sale_update(request, pk):
    sale = get_object_or_404(
        Sale,
        pk=pk
    )

    form = SaleForm(
        request.POST or None,
        instance=sale
    )

    if form.is_valid():
        form.save()
        return redirect("sale_list")

    return render(
        request,
        "sales/sale_form.html",
        {"form": form}
    )




@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(
        Sale,
        pk=pk
    )

    sale.delete()

    return redirect("sale_list")