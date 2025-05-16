from django.contrib import admin
from django.urls import path
from sg.views import UserRegistrationView
from sg.views import UserLoginView,UserProfileView,UserChangePasswordView

urlpatterns = [
    path('',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserChangePasswordView.as_view(),name='change_password'),
]