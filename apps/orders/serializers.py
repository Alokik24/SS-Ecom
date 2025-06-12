from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from apps.products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'created_at', 'note']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'status',
            'created_at', 'updated_at', 'total', 'shipping_cost', 'tax',
            'items', 'status_history'
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at', 'user']
