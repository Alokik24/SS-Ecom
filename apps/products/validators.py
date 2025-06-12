from rest_framework import serializers

def validate_image_size(value):
    """
    Validates that the uploaded image is under 2MB.
    """
    if value.size > 2 * 1024 * 1024:
        raise serializers.ValidationError("Image too big (Max 2MB)")
    return value

def validate_product_data(data):
    """
    Validates product name and price presence.
    """
    errors = {}
    if data.get('name') in [None, '']:
        errors['name'] = 'Name is required'
    if data.get('price') is None:
        errors['price'] = 'Price is required'
    if errors:
        raise serializers.ValidationError(errors)
    return data

def validate_price_positive(value):
    """
    Validates that the price of a product is positive.
    """
    if value <= 0:
        raise serializers.ValidationError("Price must be positive")
    return value
