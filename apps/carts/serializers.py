from rest_framework import serializers
from .models import Cart, CartItem
from ..products.models import Product
from ..products.serializers import ProductSerializer
from decimal import Decimal, ROUND_HALF_UP

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    product_details = ProductSerializer(source='product', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_details', 'quantity', 'total_price']

    def get_total_price(self, obj):
        price = obj.product.discount_price or obj.product.price or 0
        return price * obj.quantity

    def validate_quantity(self, value):
        """Ensure quantity is at least 1."""
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def update(self, instance, validated_data):
        """Prevent product change during update."""
        validated_data.pop('product', None)
        return super().update(instance, validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_value = serializers.SerializerMethodField()
    coupon = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'coupon', 'items', 'total_cart_value']
        read_only_fields = ['user', 'created_at']

    def get_total_cart_value(self, obj):
        items = obj.items.select_related('product')
        subtotal = sum(
            ((item.product.discount_price or item.product.price or Decimal("0.00")) * item.quantity).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP)
            for item in items
        )
        if obj.coupon and obj.coupon.active:
            discount = obj.coupon.discount_percent
            return (subtotal * Decimal(1 - discount / 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return subtotal
