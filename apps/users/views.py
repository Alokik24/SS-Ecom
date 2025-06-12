from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.views import APIView
from .permissions import IsAdmin, IsVendor, IsCustomer

class HelloView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({'message': 'Welcome to the SSEcom API'})

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({'message': 'Welcome to the SSEcom Admin'})

class VendorOnlyView(APIView):
    permission_classes = [IsVendor]

    def get(self, request):
        return Response({'message': 'Welcome to the SSEcom Vendor View'})

class CustomerOnlyView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        return Response({'message': 'Welcome to the SSEcom Customer'})
