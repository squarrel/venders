import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import Product
from user_profile.models import UserProfile


class TestViews(APITestCase):
    def setUp(self):
        user = self.user = User.objects.create(username='ringo')
        user.set_password('password123')
        user.save()
        user_profile = self.user_profile = UserProfile.objects.create(
            user=user,
            role=UserProfile.BUYER,
            deposit=0
        )

        user_seller = User.objects.create(username='john')
        user_seller.set_password('password123')
        user_seller.save()
        user_profile = UserProfile.objects.create(
            user=user_seller,
            role=UserProfile.SELLER
        )

    def test_deposit__anonymous_user(self):
        response = self.client.get(reverse('deposit', kwargs={'amount': 100}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_deposit__success(self):
        self.client.login(username='ringo', password='password123')
        response = self.client.get(reverse('deposit', kwargs={'amount': 100}))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_deposit__invalid_amount(self):
        self.client.login(username='ringo', password='password123')
        response = self.client.get(reverse('deposit', kwargs={'amount': 103}))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_deposit__forbidden_for_seller(self):
        self.client.login(username='john', password='password123')
        response = self.client.get(reverse('deposit', kwargs={'amount': 100}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_buy__product_does_not_exist(self):
        self.client.login(username='ringo', password='password123')
        data = {'1': 4, '2': 2}
        response = self.client.post(
            reverse('buy'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy__success(self):
        p1 = Product.objects.create(
            product_name='Cake',
            seller=self.user,
            amount_available=8,
            cost=220
        )
        p2 = Product.objects.create(
            product_name='Pie',
            seller=self.user,
            amount_available=6,
            cost=50
        )
        self.user_profile.deposit = 500
        self.user_profile.save()
        self.client.login(username='ringo', password='password123')
        data = {'1': 1, '2': 2}
        response = self.client.post(
            reverse('buy'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
