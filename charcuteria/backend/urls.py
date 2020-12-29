
from django.contrib import admin
from django.urls import path, include
from backend.views import  UserRegistrationView, UserLoginView

urlpatterns = [
    path('auth/signin', UserLoginView.as_view()),
    path('auth/signup', UserRegistrationView.as_view()),
]
