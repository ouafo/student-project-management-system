from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:projekt_id>/',views.chat_view, name='chat'),
]