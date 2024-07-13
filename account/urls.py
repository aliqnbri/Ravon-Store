from django.urls import path
from account import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name = 'register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verify_otp/', views.VerifyOtp.as_view(), name='otp')
]