from django.db import models
from django.conf import settings
from apps.products.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlists")
    products = models.ManyToManyField(Product, related_name="wishlisted_by")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s wishlist"