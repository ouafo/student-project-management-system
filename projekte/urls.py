from django.urls import path
from . import views

urlpatterns = [
    path('', views.projekt_detail, name='projekt_detail_liste'),
    path('<int:projekt_id>/', views.projekt_detail, name='projekt_detail'),
    path('erstellen/', views.projekt_erstellen, name='projekt_erstellen'),
    path('loeschen/<int:projekt_id>/', views.projekt_loeschen, name='projekt_loeschen'),
    path('profil/bearbeiten/', views.profil_bearbeiten, name='profil_bearbeiten'),
    path('einstellungen/', views.einstellungen, name='einstellungen'),
]