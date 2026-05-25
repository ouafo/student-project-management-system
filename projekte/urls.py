from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('projekt/erstellen', views.projekt_erstellen, name='projekt_erstellen'),
    path('projekt-loeschen/<int:projekt_id>/', views.projekt_loeschen, name='projekt_loeschen'),
    path('profil/bearbeiten/', views.profil_bearbeiten, name='profil_bearbeiten'),
    path('einstellungen/', views.einstellungen, name='einstellungen'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)