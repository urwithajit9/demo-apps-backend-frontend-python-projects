from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Product


def index(request):
    products = Product.objects.all().order_by("-created_at")[:10]
    return render(request, "core/index.html", {"products": products})


def search_products(request):
    search_query = request.GET.get("q", "")

    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) | Q(category__icontains=search_query)
        )
    else:
        products = Product.objects.all().order_by("-created_at")[:10]

    return render(request, "core/partials/results.html", {"products": products})
