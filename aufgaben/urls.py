from django.urls import path
from . import views

app_name = "aufgaben"

urlpatterns = [
    path("", views.kanban_board, name="kanban_board"),
    path("neu/", views.aufgabe_erstellen, name="aufgabe_erstellen"),
    path("chat/", views.chat_view, name="chat"),
    path("<int:pk>/", views.aufgabe_detail, name="aufgabe_detail"),
    path("<int:pk>/bearbeiten/", views.aufgabe_bearbeiten, name="aufgabe_bearbeiten"),
    path("<int:pk>/loeschen/", views.aufgabe_loeschen, name="aufgabe_loeschen"),
    path("<int:pk>/status/", views.aufgabe_status_aktualisieren, name="aufgabe_status_aktualisieren"),
    path("chat/", views.chat_view, name="chat"),
]