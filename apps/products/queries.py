from .models import Product,Category

def get_all_products_queryset():
    return Product.objects.all()

def get_all_categories_queryset():
    return Category.objects.all()

def get_product_by_slug(slug):
    return Product.objects.filter(slug=slug).first()