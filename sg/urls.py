from django.contrib import admin
from django.urls import path
from sg.views import UserRegistrationView

urlpatterns = [
    path('',UserRegistrationView.as_view(),name='santos')
]