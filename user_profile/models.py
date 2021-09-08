from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    BUYER = 'buyer'
    SELLER = 'seller'
    ROLES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=18, choices=ROLES, default=BUYER)
    deposit = models.IntegerField(default=0)
