from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_profile.models import UserProfile


class TestViews(APITestCase):
    def setUp(self):
        user = User.objects.create(username='ringo')
        user.set_password('password123')
        user.save()
        user_profile = UserProfile.objects.create(
            user=user,
            role=UserProfile.BUYER,
            deposit=0
        )

    def test_deposit__anonymous_user(self):
        response = self.client.get(reverse('deposit', kwargs={'amount': 100}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

