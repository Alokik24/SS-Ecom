from apps.carts.models import Cart
from .models import Order, OrderStatusHistory

def get_user_cart(user):
    return (
        Cart.objects
        .select_related('coupon')
        .prefetch_related('items__product')
        .filter(user=user)
        .first()
    )

def get_user_orders(user):
    return Order.objects.filter(user=user)

def get_order_status_history(user, order):
    return OrderStatusHistory.objects.filter(order__user=user, order_id=order.id)

def get_order_status_history_for_user(user, order_id=None):
    qs = OrderStatusHistory.objects.filter(order__user=user)
    if order_id:
        qs = qs.filter(order_id=order_id)
    return qs
