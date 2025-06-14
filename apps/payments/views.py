from decimal import Decimal, InvalidOperation
from django.shortcuts import render
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import PaymentTransaction
from apps.orders.models import Order, OrderStatusHistory
from .serializers import PaymentTransactionSerializer, CreateCheckoutSessionSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateCheckoutSessionSerializer  # So Swagger shows it

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            amount = Decimal(str(order.total)).quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError, ValueError):
            return Response({'message': 'Invalid order amount'}, status=status.HTTP_400_BAD_REQUEST)

        if not amount or amount <= 0:
            return Response({'message': 'Order amount must be greater than zero'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'USD',
                        'unit_amount': int(amount * 100),  # Safe now
                        'product_data': {
                            'name': 'SSEcom order',
                        },
                    },
                    'quantity': 1,
                }],
                success_url=f"{settings.FRONTEND_URL}/payment-success",
                cancel_url=f"{settings.FRONTEND_URL}/payment-cancelled",
                customer_email=request.user.email,
            )

            PaymentTransaction.objects.create(
                user=request.user,
                order=order,
                amount=amount,
                currency='USD',
                stripe_checkout_session_id=checkout_session.id
            )

            return Response({'checkout_url': checkout_session.url}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

stripe.api_key = settings.STRIPE_SECRET_KEY

class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        session_id = request.data.get('session_id')

        if not session_id:
            return Response({'message': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = PaymentTransaction.objects.get(
                stripe_checkout_session_id=session_id,
                user=request.user
            )
        except PaymentTransaction.DoesNotExist:
            return Response({'message': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

            transaction.stripe_payment_intent = payment_intent.id
            transaction.status = payment_intent.status  # 'succeeded', 'requires_payment_method', etc.
            transaction.save()

            # Optional: update order status if payment succeeded
            if payment_intent.status == 'succeeded' and transaction.order:
                if transaction.order.status == 'pending':
                    transaction.order.status = 'processing'
                    transaction.order.save()

                    OrderStatusHistory.objects.create(
                        order=transaction.order,
                        status='processing',
                        note='Payment verified via Stripe'
                    )

            return Response({
                'message': 'Payment verified',
                'status': transaction.status
            }, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)