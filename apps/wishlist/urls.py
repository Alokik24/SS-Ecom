from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]
