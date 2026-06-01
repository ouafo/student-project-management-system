from django.urls import path

from . import views



urlpatterns = [
    path('', views.projekt_detail, name='projekt_detail_liste'),
    path('projekt/erstellen/', views.projekt_erstellen, name='projekt_erstellen'),  # + Slash!
    path('projekte/<int:projekt_id>/', views.projekt_detail, name='projekt_detail'), # ← NEU
    path('projekt-loeschen/<int:projekt_id>/', views.projekt_loeschen, name='projekt_loeschen'),
    path('konto-loeschen/', views.konto_loeschen_view, name='konto_loeschen'),      # ← NEU
    path('benachrichtigung/lesen/<int:pk>/', views.benachrichtigung_lesen, name='benachrichtigung_lesen'),
    path('suche/', views.globale_suche, name='globale_suche'),
    path('profil/bearbeiten/', views.profil_bearbeiten, name='profil_bearbeiten'),
    path('einstellungen/', views.einstellungen, name='einstellungen'),
]

