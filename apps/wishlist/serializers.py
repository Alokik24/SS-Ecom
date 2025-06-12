from rest_framework import serializers
from .models import Wishlist
from apps.products.serializers import ProductSerializer

class WishlistAddRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'products', 'updated_at']
