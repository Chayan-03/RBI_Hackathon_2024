from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login')
    
]