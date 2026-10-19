from django.shortcuts import  render, redirect, get_object_or_404


from .models import Customer
from .forms import CustomerForm

from django.contrib.auth.decorators import login_required

@login_required
def customer_list(request):
    customers = Customer.objects.all()

    return render(
        request,
        "customers/customer_list.html",
        {"customers": customers}
    )

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("customer_list")

    return render(
        request,
        "customers/customer_form.html",
        {"form": form}
    )

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    form = CustomerForm(
        request.POST or None,
        instance=customer
    )

    if form.is_valid():
        form.save()
        return redirect("customer_list")

    return render(
        request,
        "customers/customer_form.html",
        {"form": form}
    )

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    customer.delete()

    return redirect("customer_list")
