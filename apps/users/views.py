from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, OTPVerifySerializer, Disable2FASerializer
from rest_framework.views import APIView
from .permissions import IsAdmin, IsVendor, IsCustomer
import pyotp
import qrcode
import io
import base64

class HelloView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({'message': 'Welcome to the SSEcom API'})

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]  # ✅ Fix here
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user

        if user.is_2fa_enabled and not user.is_2fa_verified:
            return Response({
                "2fa_required": True,
                "message": "2FA required. Scan QR and verify OTP.",
                "access": serializer.validated_data.get('access'),
                "refresh": serializer.validated_data.get('refresh'),
            }, status=200)

        return Response({
            "access": serializer.validated_data.get('access'),
            "refresh": serializer.validated_data.get('refresh'),
            "2fa_required": False
        }, status=200)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_2fa_verified = False
        user.save()
        return Response({"message": "Logged out successfully."}, status=200)

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

class Generate2FASetupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user

        # Generate new secret
        secret = pyotp.random_base32()
        user.totp_secret = secret
        user.is_2fa_enabled = True
        user.save()

        # Generate provisioning URI
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="SSecom"
        )

        # Create QR code image
        img = qrcode.make(uri)
        buffer = io.BytesIO()
        img.save(buffer)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        return Response(
            {
                "qr_code_base64": qr_base64,
                "secret": secret # Only send during setup
            }
        )

class Verify2FAView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        user = request.user

        if not user.totp_secret:
            return Response({'error': '2FA not setup'}, status=status.HTTP_400_BAD_REQUEST)

        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(otp):
            user.is_2fa_verified = True
            user.save()
            return Response({'message': '2FA verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class Disable2FAView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Disable2FASerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        password = serializer.validated_data['password']
        otp = serializer.validated_data['otp']
        
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_2fa_enabled and user.totp_secret:
            totp = pyotp.TOTP(user.totp_secret)
            if otp and not totp.verify(otp):
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user.totp_secret = None
        user.is_2fa_enabled = False
        user.is_2fa_verified = False
        user.save()

        return Response({'message': '2FA disabled'}, status=status.HTTP_200_OK)
