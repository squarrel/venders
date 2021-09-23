from django.contrib.auth.models import User
from rest_framework import serializers
from product.models import Product


class UserRelatedField(serializers.RelatedField):
    def to_representation(self, obj):
        return {'email': obj}


class ProductSerializer(serializers.ModelSerializer):
    seller = UserRelatedField(source='seller.email', read_only=True)

    class Meta:
        model = Product
        fields = ['product_name', 'seller', 'amount_available', 'cost']

    def create(self, validated_data, user):
        product = Product.objects.create(
            seller=user,
            product_name=validated_data.pop('product_name'),
            amount_available=validated_data.pop('amount_available'),
            cost=validated_data.pop('cost'),
        )
        return product
