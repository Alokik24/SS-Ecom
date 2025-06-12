from decimal import Decimal
from .models import Order, OrderStatusHistory, OrderItem

def place_order_from_cart(user, cart):
    subtotal = sum(item.total for item in cart.items.all())
    shipping_cost = Decimal('50.00')
    tax = (subtotal * Decimal('0.1')).quantize(Decimal('0.01'))
    discount = Decimal('0.00')

    if cart.coupon and cart.coupon.active:
        discount = (subtotal * Decimal(cart.coupon.discount_percent) / Decimal('100')).quantize(Decimal('0.01'))

    total = subtotal + shipping_cost + tax - discount

    order = Order.objects.create(
        user=user,
        total=total,
        shipping_cost=shipping_cost,
        tax=tax,
    )

    order_items = [
        OrderItem(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.discount_price or item.product.price
        )
        for item in cart.items.all()
    ]
    OrderItem.objects.bulk_create(order_items)

    OrderStatusHistory.objects.create(order=order, status=order.status)
    cart.items.all().delete()
    return order

def cancel_user_order(user, order, reason):
    # Ensure user owns the order
    if order.user != request.user:
        raise PermissionError("Unauthorized")

    if order.status not in ['pending', 'processing']:
        raise ValueError("Order cannot be cancelled anymore.")

    order.status = 'canceled'
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        status='canceled',
        note=f"{user} canceled order. Reason: {reason}"
    )

    return order