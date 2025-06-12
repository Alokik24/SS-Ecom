from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from apps.products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import get_tokens_for_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            return get_tokens_for_user(user)
        raise serializers.ValidationError('Invalid credentials')
