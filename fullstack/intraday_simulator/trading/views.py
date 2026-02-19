from django.shortcuts import render, redirect
from .models import Stock, Order
from .forms import OrderForm
import random


def home(request):
    stocks = Stock.objects.all()
    return render(request, "trading/home.html", {"stocks": stocks})


def simulate(request):
    price_data = {}
    stocks = Stock.objects.all()

    for stock in stocks:
        price_data[stock.id] = round(random.uniform(5, 100), 2)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("simulate")
    else:
        form = OrderForm()

    orders = Order.objects.all()
    # Auto action logic can be expanded here
    return render(
        request,
        "trading/simulate.html",
        {"form": form, "orders": orders, "price_data": price_data, "stocks": stocks},
    )
