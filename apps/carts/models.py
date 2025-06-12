from django.db import models
from django.conf import settings

from apps.products.models import Product

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField(default=10)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('Coupon', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Cart {self.id} - {self.user.email}"

    @property
    def total_price(self):
        return sum(item.total for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} (x {self.quantity})"

    @property
    def total(self):
        price = self.product.price or self.product.discount_price or 0
        return price * self.quantity

