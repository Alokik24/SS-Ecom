from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderStatusHistory, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, OrderStatusHistorySerializer
from apps.carts.models import Cart
from .queries import get_user_orders, get_user_cart, get_order_status_history_for_user
from .services import place_order_from_cart, cancel_user_order

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_orders(self.request.user)

    @action(detail=False, methods=['post'])
    def place_order(self, request):
        cart = get_user_cart(request.user)

        if not cart or not cart.items.exists():
            return Response({'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        order = place_order_from_cart(cart)
        return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()

        try:
            cancel_user_order(order, request.user, request.data.get('reason', ''))
        except PermissionError:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Order cancelled successfully"}, status=status.HTTP_200_OK)

class OrderStatusHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = OrderStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.request.query_params.get('order_id')
        return get_order_status_history_for_user(self.request.user, order_id)
