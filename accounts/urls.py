from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.startseite, name='startseite'),
    path("username-vergessen/",views.username_vergessen,name="username_vergessen"),
]