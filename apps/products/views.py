from rest_framework import generics, permissions, filters, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from apps.users.permissions import IsCustomer, IsAdmin, IsVendor
from . import queries

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = queries.get_all_products_queryset()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['category', 'brand', 'price']
    search_fields = ('name', 'description', 'brand')
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsVendor()]
        return [permissions.AllowAny()]

    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetailView(generics.RetrieveAPIView):
    queryset = queries.get_all_products_queryset()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = queries.get_all_categories_queryset()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.AllowAny()]