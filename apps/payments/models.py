from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_METHOD = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
    )

    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.transaction_id


class Refund(models.Model):
    REFUND_STATUS = (
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('processed', 'Processed'),
        ('rejected', 'Rejected'),
    )

    payment = models.ForeignKey(Payment, related_name='refunds', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Refund for {self.payment.transaction_id}"