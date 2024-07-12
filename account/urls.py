from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name = 'register'),
    path('verify_otp/', views.VerifyOtp.as_view(), name='otp')
]