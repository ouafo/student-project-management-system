from django.urls import path
from . import views

urlpatterns = [
    path('registrierung/', views.registrierung, name='registrierung'),
    path('login/', views.benutzer_login, name='login'),
    path('logout/', views.benutzer_logout, name='logout'),
]