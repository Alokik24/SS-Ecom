from decimal import Decimal, InvalidOperation
from .models import Order, OrderStatusHistory, OrderItem
import logging

logger = logging.getLogger(__name__)

def safe_decimal(value, fallback=Decimal('0.00')):
    try:
        return Decimal(str(value)).quantize(Decimal('0.01'))
    except (InvalidOperation, TypeError, ValueError):
        logger.warning(f"[Order] Invalid decimal input encountered: {value!r}")
        return fallback

def place_order_from_cart(user, cart):
    try:
        # Calculate subtotal safely
        subtotal = sum(safe_decimal(item.total) for item in cart.items.all())

        shipping_cost = Decimal('50.00')
        tax = (subtotal * Decimal('0.10')).quantize(Decimal('0.01'))
        discount = Decimal('0.00')

        # Apply coupon if available
        if cart.coupon and cart.coupon.active:
            discount_percent = safe_decimal(cart.coupon.discount_percent, Decimal('0'))
            discount = (subtotal * discount_percent / Decimal('100')).quantize(Decimal('0.01'))

        total = (subtotal + shipping_cost + tax - discount).quantize(Decimal('0.01'))

        # Create the order
        order = Order.objects.create(
            user=user,
            total=total,
            shipping_cost=shipping_cost,
            tax=tax,
        )

        # Create order items
        order_items = []
        for item in cart.items.all():
            product_price = safe_decimal(item.product.discount_price or item.product.price)
            order_items.append(OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=product_price,
            ))
        OrderItem.objects.bulk_create(order_items)

        # Record initial order status
        OrderStatusHistory.objects.create(order=order, status=order.status)

        # Clear cart
        cart.items.all().delete()

        return order

    except Exception as e:
        logger.exception(f"Order placement failed for user {user.id}: {e}")
        raise ValueError(f"Order placement failed: {str(e)}")

def cancel_user_order(user, order, reason):
    # Ensure user owns the order
    if order.user != user:
        raise PermissionError("Unauthorized")

    if order.status not in ['pending', 'processing']:
        raise ValueError("Order cannot be cancelled anymore.")

    order.status = 'cancelled'
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        status='canceled',
        note=f"{user} canceled the order. Reason: {reason}"
    )

    return order
