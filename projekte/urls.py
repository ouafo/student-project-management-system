from django.urls import path
from . import views
from .apps import ProjekteConfig

urlpatterns = [
    path('', views.my_view, name='project_view'),
]