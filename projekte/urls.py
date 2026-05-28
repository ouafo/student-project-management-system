from django.urls import path
from . import views

urlpatterns = [
    path('', views.projekt_liste, name='projekt_liste'),
    path('<int:projekt_id>/', views.projekt_detail, name='projekt_detail'),

]