from django.contrib import admin
from .models import Coupon

# Register your models here.
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'active', 'created_at']
    search_fields = ['code']