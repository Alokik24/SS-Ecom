from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, HelloView, ProfileView, AdminOnlyView, CustomerOnlyView, VendorOnlyView, Generate2FASetupView, Verify2FAView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', AdminOnlyView.as_view(), name='admin_view'),
    path('customer/', CustomerOnlyView.as_view(), name='customer_view'),
    path('vendor/', VendorOnlyView.as_view(), name='vendor_view'),
    path('2fa/setup/', Generate2FASetupView.as_view()),
    path('2fa/verify/', Verify2FAView.as_view()),
    path('logout/', LogoutView.as_view()),
]