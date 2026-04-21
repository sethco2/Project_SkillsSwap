"""URL patterns for the accounts app."""
from django.urls import path
from . import views

urlpatterns = [
    # /accounts/register/  -> shows signup form / creates user
    path('register/', views.register, name='register'),
]
