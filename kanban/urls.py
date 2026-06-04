from django.urls import path
from . import views

urlpatterns = [
    path('<int:projekt_id>/',
         views.kanban_board,
         name='kanban_board'),
    path('aufgabe/<int:aufgabe_id>/status/',
         views.aufgabe_status_update,
         name='aufgabe_status_update'),
]