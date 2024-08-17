from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenVerifyView
app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
 
    path('login/',views.CustomLoginView.as_view() , name='login'),
    path('verifyotp/',views.VerifyTemplateView.as_view(),name='verifyotp'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='token_obtain_pair'),
    path('verify-otp/', views.VerifyOtp.as_view(), name='verify-otp'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
