from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.users.permissions import IsCustomer
from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer
from .services import add_item_to_cart, increment_cart_item, decrement_or_remove_cart_item
from .queries import get_or_create_cart, get_coupon_by_code

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsCustomer()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        cart, created = get_or_create_cart(self.request.user)
        if not created:
            serializer.instance = cart
        else:
            serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        cart, _ = get_or_create_cart(request.user)
        total_price = sum(item.total for item in cart.items.all())
        item_count = cart.items.count()
        return Response({'total_price': total_price, 'item_count': item_count})

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart, _ = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response({"message": "Cart cleared successfully"})

    @action(detail=False, methods=['post'])
    def apply_coupon(self, request):
        code = request.data.get('code')
        coupon = get_coupon_by_code(code)
        if not coupon:
            return Response({"message": "Invalid or expired coupon"}, status=status.HTTP_400_BAD_REQUEST)
        cart, _ = get_or_create_cart(request.user)
        cart.coupon = coupon
        cart.save()
        return Response({'message': f'Coupon "{code}" applied successfully'})

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCustomer()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        cart_item, _ = add_item_to_cart(self.request.user, product, quantity)
        serializer.instance = cart_item

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['post'])
    def increment(self, request, pk=None):
        item = self.get_object()
        increment_cart_item(item)
        return Response({"quantity": item.quantity}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def decrement(self, request, pk=None):
        item = self.get_object()
        status_msg, quantity = decrement_or_remove_cart_item(item)
        if status_msg == "removed":
            return Response({"message": "Item removed from the cart"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"quantity": quantity}, status=status.HTTP_200_OK)
