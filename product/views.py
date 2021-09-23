from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.permissions import IsOwnerOrReadOnly
from product.serializers import ProductSerializer
from user_profile.models import UserProfile


class ProductView(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, product)

        return product

    def get(self, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid(raise_exception=ValueError):
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role != UserProfile.SELLER:
                return JsonResponse(
                    {'message': 'Creating products only allowed to users with seller role.'},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

            serializer.create(validated_data=request.data, user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
