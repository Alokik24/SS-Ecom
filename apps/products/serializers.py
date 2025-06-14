from rest_framework import serializers
from .models import Product, Category
from apps.users.serializers import UserSerializer
from .validators import (
    validate_image_size,
    validate_product_data,
    validate_price_positive,
)
from .services import assign_vendor
from decimal import Decimal, InvalidOperation

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'slug', 'subcategories']

    def get_subcategories(self, obj):
        request = self.context.get('request', None)
        if request and request.method in ['GET']:
            return SubCategorySerializer(obj.subcategories.all(), many=True).data
        return None

class ProductSerializer(serializers.ModelSerializer):
    vendor = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category',
    )
    absolute_url = serializers.SerializerMethodField()
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'brand', 'price', 'discount_price',
            'stock_quantity', 'in_stock', 'category', 'category_id',
            'vendor', 'image', 'created_at', 'absolute_url'
        ]

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def create(self, validated_data):
        validated_data = assign_vendor(validated_data, self.context['request'].user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = assign_vendor(validated_data, self.context['request'].user)
        return super().update(instance, validated_data)

    def validate_image(self, value):
        return validate_image_size(value)

    def validate(self, data):
        data['price'] = validate_price_positive(data.get('price', 0))

        discount = data.get('discount_price')
        if discount is not None:
            try:
                data['discount_price'] = Decimal(str(discount)).quantize(Decimal("0.01"))
            except (InvalidOperation, ValueError, TypeError):
                raise serializers.ValidationError({
                    "discount_price": "Invalid discount format. Must be a number with up to 2 decimal places."
                })
        return validate_product_data(data)

    def validate_price_positive(value):
        try:
            value = Decimal(str(value)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError, TypeError):
            raise serializers.ValidationError("Invalid price format. Must be a number with 2 decimal places.")

        if value < 0:
            raise serializers.ValidationError("Price must be positive.")

        return value

    def validate_price(self, value):
        return validate_price_positive(value)


