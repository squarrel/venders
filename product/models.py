from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=55)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_available = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
