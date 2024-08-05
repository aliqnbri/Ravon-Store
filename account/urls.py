from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='token_obtain_pair'),
    path('verify-otp/', views.VerifyOtp.as_view(), name='verify-otp'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('login/', views.LoginView.as_view()),
    # path('profile/', views.ProfileView.as_view()),
    # path('profile/update/', views.UpdateProfileView.as_view()),
    # path('profile/update/password/', views.UpdatePasswordView.as_view()),
    # path('profile/update/phone_number/', views.UpdatePhoneView.as_view()),
    # path('profile/update/email/', views.UpdateEmailView.as_view()),


]
