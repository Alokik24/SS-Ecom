from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistAddRemoveSerializer
from apps.products.models import Product
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .queries import (
    get_or_create_user_wishlist,
    add_product_to_wishlist,
    remove_product_from_wishlist
)

class WishlistViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer
    def list(self, request):
        wishlist = get_or_create_user_wishlist(request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=WishlistAddRemoveSerializer,
        responses={200: openapi.Response('Added to wishlist')}
    )
    @action(detail=False, methods=['post'], url_path='add')
    def add(self, request):
        serializer = WishlistAddRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']

        try:
            product = Product.objects.get(id=product_id)
            wishlist = add_product_to_wishlist(request.user, serializer.validated_data['product_id'])
            return Response({'message': 'Added to wishlist.'})
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=404)

    @swagger_auto_schema(
        request_body=WishlistAddRemoveSerializer,
        responses={200: openapi.Response('Removed from wishlist')}
    )
    @action(detail=False, methods=['post'], url_path='remove')
    def remove(self, request):
        serializer = WishlistAddRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']

        try:
            wishlist = remove_product_from_wishlist(request.user, product_id)
            return Response({'message': 'Removed from wishlist.'})
        except Exception:
            return Response({'error': 'Failed to remove.'}, status=400)
