from django.urls import path
from . import views

urlpatterns = [
    path('request/<order_id>', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
    path('callback/', views.CallBackTemplateView.as_view(), name ='callback')
]