from django.urls import path
from . import views

urlpatterns = [
    path("neu/", views.aufgabe_erstellen, name="aufgabe_erstellen"),
    path("neu/<int:projekt_id>/", views.aufgabe_erstellen, name="aufgabe_erstellen_projekt"),
    path("<int:pk>/", views.aufgabe_detail, name="aufgabe_detail"),
    path("<int:pk>/bearbeiten/", views.aufgabe_bearbeiten, name="aufgabe_bearbeiten"),
    path("<int:pk>/loeschen/", views.aufgabe_loeschen, name="aufgabe_loeschen"),
]