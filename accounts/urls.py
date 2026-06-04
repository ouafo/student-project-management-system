from django.urls import path
from . import views

urlpatterns = [
    path('',views.startseite,name='startseite'),
    path('register/',views.register,name='register'),
    path('username-vergessen/',views.username_vergessen,name='username_vergessen'),

    path('login/', views.benutzer_login, name='login'),
    path('logout/', views.benutzer_logout, name='logout'),
]