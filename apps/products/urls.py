from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductDetailView, CategoryViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
urlpatterns = router.urls + [
               path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail')
]