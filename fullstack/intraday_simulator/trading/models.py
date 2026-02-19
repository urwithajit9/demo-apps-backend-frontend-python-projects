from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Order(models.Model):
    ORDER_TYPE = [("BUY", "Buy"), ("SELL", "Sell")]
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    stop_loss = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
