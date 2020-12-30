from django.contrib import admin
from django.urls import path, include
from backend.views import  UserRegistrationView, UserLoginView, product_list, product_details

urlpatterns = [
    path('auth/signin', UserLoginView.as_view()),
    path('auth/signup', UserRegistrationView.as_view()),
    
    path('productos', product_list),
    path('productos/<int:id>', product_details)
]