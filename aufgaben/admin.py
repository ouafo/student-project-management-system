from django.contrib import admin
from .models import Aufgabe
# Register your models here.


@admin.register(Aufgabe)
class AufgabeAdmin(admin.ModelAdmin):
    list_display = ['titel', 'projekt', 'status', 'prioritaet', 'zugewiesen_an', 'deadline']
    list_filter = ['status', 'prioritaet']