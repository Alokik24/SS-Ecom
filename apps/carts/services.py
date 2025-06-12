from .queries import get_or_create_cart, get_cart_item
from .models import CartItem

def add_item_to_cart(user, product, quantity):
    cart, _ = get_or_create_cart(user)
    cart_item = get_cart_item(cart, product)
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
        return cart_item, False
    else:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        return cart_item, True

def increment_cart_item(item):
    item.quantity += 1
    item.save()
    return item.quantity

def decrement_or_remove_cart_item(item):
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        return "decremented", item.quantity
    else:
        item.delete()
        return "removed", 0
