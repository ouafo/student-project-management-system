from django.urls import path
from .views import register, activate

urlpatterns = [
    path("register/", register, name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
