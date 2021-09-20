from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from user_profile.decorators import only_buyers
from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class UserProfileView(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, format=None):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user_profile = self.get_object(pk)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_profile = self.get_object(pk=pk)
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
@only_buyers
def deposit(request, amount):
    if amount not in UserProfile.ALLOWED_COINS:
        return JsonResponse(
            {'message': 'Invalid amount.'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )

    user_profile = UserProfile.objects.get(user__pk=request.user.pk)
    user_profile.deposit += amount
    user_profile.save()

    return JsonResponse(
        {'message': 'Success'},
        status=status.HTTP_202_ACCEPTED
    )


@api_view()
@only_buyers
def buy(request):
    data = request.data
    user_profile = UserProfile.objects.get(user=request.user)

    total_price = 0
    bought_products = list()

    for pk, amount in data.items():
        product = Product.objects.get(pk=pk)
        total_price += product.cost * amount
        bought_products.append(product.product_name)

    if not user_profile.deposit >= total_price:
        return JsonResponse(
            {'message': 'Action failed. Insufficient user deposit.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_profile.deposit -= total_price
    user_profile.save()

    resp_data = {
        'total_spent': total_price,
        'change': user_profile.deposit,
        'products': bought_products
    }

    return JsonResponse(
        {'message': 'Successful purchase.', 'data': resp_data},
        status=status.HTTP_202_ACCEPTED
    )
