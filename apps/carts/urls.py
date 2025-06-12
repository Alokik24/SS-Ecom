from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, CartViewSet
from ..products.views import ProductViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('carts', CartViewSet, basename='carts')
router.register('cart-items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
]