from rest_framework import serializers
from .models import PaymentTransaction

class PaymentTransactionSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()

    class Meta:
        model = PaymentTransaction
        fields = '__all__'
        read_only_fields = ['status', 'stripe_checkout_session_id']

class CreateCheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()