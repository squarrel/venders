from django.contrib.auth.models import User
from rest_framework import serializers
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source='seller.email')

    class Meta:
        model = Product
        fields = ['product_name', 'seller', 'amount_available', 'cost']

    def create(self, validated_data):
        seller_data = validated_data.pop('seller')
        user = User.objects.get(email=seller_data)

        product = Product.objects.create(
            seller=user,
            product_name=validated_data.pop('product_name'),
            amount_available=validated_data.pop('amount_available'),
            cost=validated_data.pop('cost'),
        )
        return product

    def update(self, instance, validated_data):
        seller_data = validated_data.get('seller')
        user = User.objects.get(email=seller_data['email'])
        validated_data['seller'] = user

        return super().update(instance, validated_data)
