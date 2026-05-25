from django.urls import path
from . import views

urlpatterns = [
    path('', views.projekt_liste, name='projekt_liste'),
    path('<int:projekt_id>/', views.projekt_detail, name='projekt_detail'),
    path('<int:projekt_id>/kanban', views.kanban_board, name='kanban_board'),
    path('aufgabe/<int:aufgabe_id>/status/', views.aufgabe_status_update, name='aufgabe_status_update'),

]