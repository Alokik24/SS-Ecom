from .models import Cart, CartItem, Coupon
from apps.products.models import Product
from django.shortcuts import get_object_or_404

def get_or_create_cart(user):
    return Cart.objects.get_or_create(user=user)

def get_cart(user):
    return Cart.objects.filter(user=user).first()

def get_cart_items(user):
    return CartItem.objects.filter(cart__user=user)

def get_cart_item(cart, product):
    return CartItem.objects.filter(cart=cart, product=product).first()

def get_coupon_by_code(code):
    return Coupon.objects.filter(code=code, active=True).first()
