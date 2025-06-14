from django.db import models
from django.conf import settings
from apps.orders.models import Order

# Create your models here.
User = settings.AUTH_USER_MODEL

class PaymentTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_transactions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_transactions', null=True,
                              blank=True)
    stripe_checkout_session_id = models.CharField(max_length=255, unique=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, default="pending") # succeeded, failed, pending
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.status} - ${self.amount} {self.currency}"