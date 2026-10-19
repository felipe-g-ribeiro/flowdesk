from django.shortcuts import render

from products.models import Product, Category
from customers.models import Customer
from sales.models import Sale


def dashboard(request):
    context = {
        "total_products": Product.objects.count(),
        "total_categories": Category.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_sales": Sale.objects.count(),
    }

    return render(request, "core/dashboard.html", context)