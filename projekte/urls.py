from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.projekt_detail, name='projekt_detail_liste'),
    path('<int:projekt_id>/', views.projekt_detail, name='projekt_detail'),
    path('erstellen/', views.projekt_erstellen, name='projekt_erstellen'),
    path('loeschen/<int:projekt_id>/', views.projekt_loeschen, name='projekt_loeschen'),
    path('benachrichtigung/lesen/<int:pk>/', views.benachrichtigung_lesen, name='benachrichtigung_lesen'),
    path('suche/', views.globale_suche, name='globale_suche'),
    path('profil/bearbeiten/', views.profil_bearbeiten, name='profil_bearbeiten'),
    path('einstellungen/', views.einstellungen, name='einstellungen'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)