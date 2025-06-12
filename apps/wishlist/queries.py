from .models import Wishlist
from apps.products.models import Product

def get_or_create_user_wishlist(user):
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist

def add_product_to_wishlist(user, product_id):
    product = Product.objects.get(id=product_id)
    wishlist = get_or_create_user_wishlist(user)
    wishlist.products.add(product)
    return wishlist

def remove_product_from_wishlist(user, product_id):
    wishlist = get_or_create_user_wishlist(user)
    wishlist.products.remove(product_id)
    return wishlist