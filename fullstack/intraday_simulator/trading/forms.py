from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["stock", "order_type", "quantity", "price", "stop_loss"]
