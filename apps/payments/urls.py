from django.urls import path
from .views import CreateCheckoutSessionView, VerifyPaymentView
from .webhook_views import stripe_webhook
from django.http import HttpResponse

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
    path("success/", lambda request: HttpResponse("Payment Success")),
    path("cancel/", lambda request: HttpResponse("Payment Cancelled")),
]