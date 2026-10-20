"""Маршруты приложения users."""
from django.urls import path
from . import views

app_name = 'users'  # ← ОБЯЗАТЕЛЬНО должна быть эта строка

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('public/', views.public_view, name='public'),
]