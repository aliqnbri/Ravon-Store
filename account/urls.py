from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenVerifyView
app_name = 'account'

urlpatterns = [
    path('api/register/', views.RegisterUserView.as_view(), name='register'),
    path('api/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', views.LogoutView.as_view(), name='token_obtain_pair'),
    path('api/verify-otp/', views.VerifyOtp.as_view(), name='verify-otp'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/',views.CustomLoginView.as_view() , name='login'),
    path('verify-otp/', views.VerifyTemplateView.as_view(), name='verify-otp'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
 


]
